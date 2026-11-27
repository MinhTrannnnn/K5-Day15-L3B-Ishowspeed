"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    mô phỏng chọn action bằng luật đơn giản, model "fake", token 0 — để luồng chạy hết từ trước CP2 (guide bước 3.2).
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Docker Compose hỗ trợ Ollama và OpenAI. OpenRouter dùng được khi chạy Python trực tiếp.
"""
import os
import json
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_DEFAULTS = {
    'ollama': ('CP3_MODEL', 'qwen2.5:1.5b'),
    'openai': ('OPENAI_MODEL', 'gpt-5.4-nano'),
    'openrouter': ('OPENROUTER_MODEL', 'openai/gpt-4.1-mini'),
}
model_setting, default_model = MODEL_DEFAULTS.get(MODEL_PROVIDER, ('MODEL_NAME', 'fake'))
MODEL_NAME = (os.environ.get('MODEL_NAME', '').strip()
              or os.environ.get(model_setting, '').strip() or default_model)


class HostedModelError(RuntimeError):
    """Lỗi đã lược bỏ dữ liệu từ nhà cung cấp, an toàn để hiển thị ở demo local."""


def decision_schema(context):
    key = 'action'
    choices = ['wait', 'cancel_review', 'refund_status', 'human_review', 'out_of_scope']
    if context.get('allow_clarify'):
        choices.append('clarify')
    return {'type': 'object', 'properties': {key: {'type': 'string', 'enum': choices}},
            'required': [key], 'additionalProperties': False}


def call_ollama(system, user):
    base = os.environ.get('OLLAMA_URL', 'http://127.0.0.1:11434').rstrip('/')
    body = {'model': MODEL_NAME, 'stream': False, 'format': decision_schema(json.loads(user)),
            'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}],
            'options': {'temperature': 0, 'num_predict': 64, 'num_ctx': 2048}}
    request = Request(f'{base}/api/chat', headers={'Content-Type': 'application/json'},
                      data=json.dumps(body).encode('utf-8'))
    try:
        with urlopen(request, timeout=90) as response:
            result = json.load(response)
        return {'text': result['message']['content'], 'model': result['model'],
                'tokens_in': result['prompt_eval_count'], 'tokens_out': result['eval_count']}
    except HTTPError as error:
        raise RuntimeError(f'Ollama trả HTTP {error.code}. Kiểm tra model đã tải.') from error
    except (URLError, TimeoutError) as error:
        raise RuntimeError('Chưa kết nối được Ollama. Kiểm tra service model và thử lại.') from error


def call_hosted_model(system, user):
    is_openai = MODEL_PROVIDER == 'openai'
    if is_openai:
        provider, key_name = 'OpenAI', 'OPENAI_API_KEY'
        endpoint = 'https://api.openai.com/v1/chat/completions'
        options = {'max_completion_tokens': 256, 'store': False}
    else:
        provider, key_name = 'OpenRouter', 'OPENROUTER_API_KEY'
        endpoint = 'https://openrouter.ai/api/v1/chat/completions'
        options = {'temperature': 0, 'max_tokens': 128, 'provider': {'require_parameters': True}}
    api_key = os.environ.get(key_name, '').strip()
    if is_openai and not api_key:
        api_key = os.environ.get('API_KEY', '').strip()
    if not api_key:
        raise HostedModelError(f'Cần đặt {key_name} trong .env và chạy lại Docker Compose.')
    schema = decision_schema(json.loads(user))
    body = {'model': MODEL_NAME, 'stream': False, **options,
            'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}],
            'response_format': {'type': 'json_schema', 'json_schema': {
                'name': 'd1_decision', 'strict': True, 'schema': schema}}}
    request = Request(endpoint,
                      headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'},
                      data=json.dumps(body).encode('utf-8'))
    for attempt in range(3):
        try:
            with urlopen(request, timeout=60) as response:
                result = json.load(response)
            break
        except HTTPError as error:
            retry_after = error.headers.get('Retry-After', '')
            if error.code == 429 and attempt < 2 and retry_after in ('0', '1', '2', '3', '4', '5'):
                error.close()
                sleep(max(1, int(retry_after)) + attempt)
                continue
            hints = {401: 'Kiểm tra API key.', 402: 'Kiểm tra số dư hoặc hạn mức key.',
                     403: 'Kiểm tra quyền của key và dự án.', 404: 'Kiểm tra tên model và quyền truy cập.',
                     429: 'Kiểm tra số dư, hạn mức dự án hoặc thử lại sau.'}
            hint = hints.get(error.code, 'Kiểm tra model và cấu hình.')
            error.close()
            raise HostedModelError(f'{provider} trả HTTP {error.code}. {hint}') from None
        except (URLError, TimeoutError) as error:
            raise HostedModelError(f'Không kết nối được {provider}. Kiểm tra Internet và thử lại.') from error
    try:
        choice = result['choices'][0]
        text = choice['message']['content']
        usage = result['usage']
        if choice.get('finish_reason') != 'stop' or not isinstance(text, str) or not text.strip():
            raise ValueError
        return {'text': text, 'model': result['model'],
                'tokens_in': usage['prompt_tokens'], 'tokens_out': usage['completion_tokens']}
    except (IndexError, KeyError, TypeError, ValueError) as error:
        raise HostedModelError(f'{provider} không trả nội dung hoặc dữ liệu token hợp lệ.') from error


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        # Model giả mô phỏng chọn bước từ ngữ cảnh, không đọc benchmark/expected.
        context = json.loads(user)
        observed = context.get('observations', {})
        step = next((name for name in ('get_order', 'get_policy', 'order_timeline')
                     if name not in observed), 'finish')
        return {'text': json.dumps({'tool': step}), 'model': 'fake',
                'tokens_in': 0, 'tokens_out': 0}

    if MODEL_PROVIDER in ('openai', 'openrouter'):
        return call_hosted_model(system, user)
    if MODEL_PROVIDER == 'ollama':
        return call_ollama(system, user)
    raise NotImplementedError(
        "MODEL_PROVIDER=%s chưa được hỗ trợ. Dùng ollama, openai, openrouter hoặc fake."
        % MODEL_PROVIDER)
