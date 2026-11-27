import { useEffect, useRef, useState } from 'react';
import type { FormEvent } from 'react';
import { createRoot } from 'react-dom/client';
import {
  ArrowClockwiseIcon, ArrowRightIcon, ChatCircleDotsIcon, ChatTextIcon, CheckCircleIcon, ClipboardTextIcon,
  ClockIcon, PackageIcon, PaperPlaneTiltIcon, ShieldCheckIcon, StorefrontIcon, TruckIcon, UserCircleIcon,
  UserIcon, WarningCircleIcon,
} from '@phosphor-icons/react';
import './styles.css';

type Order = {order_id: string; restaurant: string; status: string; updated_at: string; eta: string | null; delay_minutes: number | null; refund: string | null};
type Draft = {order_id: string; proposal: string; conflicts: string[]; missing: string[]};
type StaffDraft = Draft & {customer_goal: string; customer_claims: string[]; sources: string[]; created_at: string; order?: Order | null};
type Case = {id: number; code: string; order_id: string; status: string; label: string; response: string; order: Order | null};
type Activity = {at: string; status: string; note: string; actor: 'customer' | 'staff'};
type Choice = {value: string; label: string};
type StaffCase = Case & {version: number; draft: StaffDraft; next_statuses: Choice[]; events: Activity[]};
type Message = {role: 'customer' | 'assistant'; text: string; choices?: string[]};
type Trace = {models: string[]; tokens_in: number; tokens_out: number};
type CustomerData = {order: Order | null; messages: Message[]; draft: Draft | null; cases: Case[]; trace?: Trace};
type StaffData = {draft: StaffDraft | null; cases: StaffCase[]};

const samples = [
  {id:'D007', label:'Đã giao, chưa nhận', text:'D007 hiện giao đến đâu rồi? Nhờ nhân viên kiểm tra giúp.'},
  {id:'D004', label:'Giao chậm, muốn hủy', text:'Tôi muốn kiểm tra khả năng hủy đơn D004.'},
  {id:'D005', label:'Đã hủy, hỏi tiền hoàn', text:'D005 khi nào hoàn tiền?'},
];
const labels: Record<string, string> = {
  received:'Đã tiếp nhận', verifying:'Đang xác minh', needs_info:'Cần bổ sung', pending_approval:'Chờ duyệt',
  in_progress:'Đang thực hiện', resolved:'Đã có kết quả',
};
const goalLabels: Record<string, string> = {cancel_review:'Muốn kiểm tra hủy', refund_status:'Hỏi khoản hoàn', wait:'Hỏi tình trạng đơn'};

async function request<T>(path: string, method = 'GET', body?: object): Promise<T> {
  const response = await fetch(`/api${path}`, {
    method, ...(body ? {headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)} : {}),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'Không xử lý được yêu cầu này.');
  return data;
}

function timestamp(value: string) {
  return new Intl.DateTimeFormat('vi-VN', {dateStyle:'short', timeStyle:'short', timeZone:'Asia/Ho_Chi_Minh'}).format(new Date(value));
}

function Badge({label, status}: {label: string; status?: string}) {
  return <span className={`badge ${status === 'resolved' ? 'complete' : ''}`}>{label}</span>;
}

function Progress({status}: {status?: string}) {
  const current = status === 'resolved' ? 2 : status && status !== 'received' ? 1 : 0;
  const first = status ? 'Đã tiếp nhận' : 'Chờ tiếp nhận';
  return <ol className="progress" aria-label="Tiến độ xử lý">
    {[first, 'Đang xác minh', 'Hoàn tất'].map((step, index) =>
      <li key={step} className={index <= current ? 'reached' : ''} aria-current={index === current ? 'step' : undefined}>
        <span className="progress-point" aria-hidden="true">{index < current ? <CheckCircleIcon size={23} weight="fill"/> : <span/>}</span>{step}
      </li>)}
  </ol>;
}

function OrderInfo({order}: {order: Order | null}) {
  if (!order) return <section className="panel details"><h2>Thông tin đơn</h2><p className="muted">Chọn đơn mẫu hoặc nhập mã đơn để kiểm tra.</p></section>;
  const rows = [
    {Icon:PackageIcon, label:'Mã đơn', value:order.order_id},
    {Icon:StorefrontIcon, label:'Quán', value:order.restaurant},
    {Icon:TruckIcon, label:'Hệ thống ghi', value:order.status},
    ...(order.eta ? [{Icon:ClockIcon, label:'Giờ giao dự kiến', value:order.eta}] : []),
    ...(order.delay_minutes ? [{Icon:ClockIcon, label:'Trễ so với dự kiến', value:`${order.delay_minutes} phút`}] : []),
    ...(order.refund ? [{Icon:ClipboardTextIcon, label:'Khoản hoàn', value:({pending:'Đang chờ xử lý',completed:'Đã hoàn tất',not_started:'Chưa ghi nhận'} as Record<string,string>)[order.refund] || 'Chưa xác minh'}] : []),
  ];
  return <section className="panel details"><h2>Thông tin đơn</h2><dl>
    {rows.map(({Icon,label,value}) => <div className="detail-row" key={label}><dt><Icon size={21}/>{label}</dt><dd>{value}</dd></div>)}
  </dl><p className="footnote">Dữ liệu demo cập nhật {timestamp(order.updated_at)}</p></section>;
}

function CustomerWorkspace({data, busy, onSend, onReset, onRefresh}: {
  data: CustomerData | null; busy: boolean; onSend: (text:string)=>void; onReset:()=>void; onRefresh:()=>void;
}) {
  const [text, setText] = useState('');
  const [selected, setSelected] = useState<number | null>(null);
  const feed = useRef<HTMLDivElement>(null);
  const messages = data?.messages || [];
  const current = data?.cases.find(item => item.id === selected) || data?.cases.find(item => item.order_id === data.order?.order_id) || (!data?.order ? data?.cases[0] : undefined);
  const draft = selected === null ? data?.draft : null;
  const order = current?.order || data?.order || null;

  useEffect(() => { if (feed.current) feed.current.scrollTop = feed.current.scrollHeight; }, [messages, busy]);

  function submit(event: FormEvent) {
    event.preventDefault();
    if (!text.trim()) return;
    const message = selected !== null && current && !/\bD\d{3,}\b/i.test(text) ? `${current.order_id} ${text.trim()}` : text.trim();
    setSelected(null);
    onSend(message);
    setText('');
  }

  return <div className="customer-grid">
    <section className="panel chat">
      <header className="chat-heading"><div className="chat-title"><ChatCircleDotsIcon size={28}/><div><h1>Trợ lý đơn hàng</h1><p className="muted">Tra cứu đơn giao chậm, hủy đơn hoặc khoản hoàn.</p></div></div>
        <button className="quiet" onClick={() => {setSelected(null); onReset();}} disabled={busy}>Bắt đầu lại</button></header>
      <div ref={feed} className="messages" role="log" aria-label="Hội thoại của khách" aria-live="polite">
        {!messages.length && <div className="chat-empty"><ChatTextIcon size={34}/><h2>Bạn cần hỗ trợ đơn nào?</h2><p>Nhập mã đơn và tình huống bạn gặp, hoặc chọn một đơn mẫu.</p></div>}
        {messages.map((message,index) => <div className={`message ${message.role}`} key={index}>
          <p>{message.text}</p>
          {index === messages.length - 1 && Boolean(message.choices?.length) && <div className="quick-replies">
            {message.choices?.map(choice => <button className="quiet" disabled={busy} key={choice} onClick={() => {setSelected(null); onSend(choice);}}>{choice.replace(/^Tôi /, '').replace(/\.$/, '')}</button>)}
          </div>}
        </div>)}
        {busy && <p className="waiting" role="status">Đang xử lý…</p>}
      </div>
      <form className="composer" onSubmit={submit}><input aria-label="Tin nhắn" placeholder="Ví dụ: D007 báo đã giao nhưng tôi chưa nhận" maxLength={990} value={text} onChange={event=>setText(event.target.value)} required/>
        <button className="primary" disabled={busy}><PaperPlaneTiltIcon size={19}/>Gửi</button></form>
    </section>
    <aside className="rail">
      <OrderInfo order={order}/>
      {(current || draft) && <section className="panel details follow-up"><div className="section-head"><h2>{current ? `Yêu cầu ${current.code}` : 'Yêu cầu xác minh'}</h2>{current && <button className="icon-button" aria-label="Làm mới trạng thái" onClick={onRefresh} disabled={busy}><ArrowClockwiseIcon size={19}/></button>}</div>
        <Badge label={current?.label || 'Chờ tiếp nhận'} status={current?.status}/>
        <p>{current?.response || 'Hồ sơ đã được chuẩn bị để nhân viên tiếp nhận.'}</p><Progress status={current?.status}/>
      </section>}
      {Boolean(data?.cases.length) && <section className="panel details"><h2>Tra cứu yêu cầu</h2>
        <select aria-label="Chọn yêu cầu" value={current?.id || ''} onChange={event=>setSelected(Number(event.target.value) || null)}>
          <option value="">Theo đơn đang chat</option>{data?.cases.map(item=><option key={item.id} value={item.id}>{item.code} · {item.order_id} · {item.label}</option>)}
        </select></section>}
      <section className="panel details"><h2>Đơn mẫu</h2><div className="sample-list">{samples.map(sample => <button key={sample.id} disabled={busy} onClick={()=>{setSelected(null); onSend(sample.text);}}><strong>{sample.id}</strong><span>{sample.label}</span><ArrowRightIcon size={17}/></button>)}</div></section>
      {Boolean(data?.trace?.tokens_out) && <details className="technical"><summary>Chi tiết model</summary><p>{data?.trace?.models.join(', ')} · {data?.trace?.tokens_in} token vào · {data?.trace?.tokens_out} token ra</p></details>}
    </aside>
  </div>;
}

function StaffWorkspace({data, selected, onSelect, busy, onReceive, onUpdate}: {
  data: StaffData | null; selected: number | null; onSelect: (id: number | null)=>void; busy: boolean;
  onReceive: ()=>void; onUpdate: (item: StaffCase,status: string,note: string)=>void;
}) {
  const [tab, setTab] = useState<'inbox'|'active'>('inbox');
  const [note, setNote] = useState('');
  const [status, setStatus] = useState('');
  const item = data?.cases.find(row=>row.id === selected);
  const draft = item?.draft || (tab === 'inbox' ? data?.draft : null);
  const next = item?.next_statuses.find(choice=>choice.value === status)?.value || item?.next_statuses[0]?.value || '';
  const order = item?.order || draft?.order || null;
  const claims = draft?.customer_claims || [];
  const latestClaim = item?.events.filter(event=>event.actor === 'customer').at(-1)?.note || claims.at(-1) || 'Chưa ghi nhận';
  const activeRows = data?.cases || [];
  useEffect(()=>{ setNote(''); setStatus(''); }, [item?.id, item?.version]);
  useEffect(()=>{ if (selected !== null) setTab('active'); }, [selected]);

  return <div className="staff-grid">
    <aside className="panel queue"><h2>Hồ sơ cần xử lý</h2>
      <div className="segments" aria-label="Lọc hồ sơ"><button aria-pressed={tab==='inbox'} onClick={()=>{setTab('inbox'); onSelect(null);}}>Tiếp nhận</button><button aria-pressed={tab==='active'} onClick={()=>{setTab('active'); onSelect(activeRows[0]?.id ?? null);}}>Đang xử lý</button></div>
      {tab === 'inbox' && data?.draft && <button className="queue-row selected" onClick={()=>onSelect(null)}><strong>{data.draft.order_id}</strong><Badge label="Chờ tiếp nhận"/><span>{samples.find(sample=>sample.id===data.draft?.order_id)?.label || 'Yêu cầu hỗ trợ đơn'}</span></button>}
      {tab === 'active' && activeRows.map(row=><button aria-current={row.id===selected ? 'true' : undefined} key={row.id} className={`queue-row ${row.id===selected ? 'selected' : ''}`} onClick={()=>onSelect(row.id)}><strong>{row.order_id} · {row.code}</strong><Badge label={row.label} status={row.status}/></button>)}
      {!(tab === 'inbox' ? data?.draft : activeRows.length) && <p className="muted queue-empty">{tab==='inbox' ? 'Chưa có yêu cầu chờ tiếp nhận.' : 'Chưa có ca đã tiếp nhận.'}</p>}
    </aside>
    <section className="panel dossier">
      {!draft ? <div className="empty-dossier"><ClipboardTextIcon size={34}/><h1>Hồ sơ hỗ trợ</h1><p className="muted">Chọn một hồ sơ trong danh sách để xem và xử lý.</p></div> : <>
        <header className="dossier-head"><div className="dossier-title"><h1>Đơn {draft.order_id}</h1><Badge label={item?.label || 'Chờ tiếp nhận'} status={item?.status}/></div>
          {!item && <button className="primary" onClick={onReceive} disabled={busy}>Tiếp nhận hồ sơ</button>}</header>
        <p className="muted summary-intro">Đối chiếu tình trạng đơn với lời khách để xác định bước xử lý.</p>
        <section className="dossier-section"><h2>Tóm tắt vụ việc</h2><div className="facts">
          <div><PackageIcon size={27}/><span>Hệ thống ghi<strong>{order?.status || 'Chưa rõ'}</strong></span></div>
          <div><UserIcon size={27}/><span>Khách báo<strong>{draft.conflicts.some(value=>value.includes('khách nói chưa nhận')) ? 'Chưa nhận món' : goalLabels[draft.customer_goal] || 'Cần hỗ trợ'}</strong></span></div>
        </div>{[...draft.conflicts, ...draft.missing].map(value=><p className="conflict" key={value}>{value}</p>)}</section>
        <section className="dossier-section"><h2>Lời khách</h2><blockquote>{latestClaim}</blockquote></section>
        <section className="dossier-section"><h2>Đề xuất</h2><div className="proposal"><ShieldCheckIcon size={27}/><div><strong>{draft.conflicts.length ? 'Xác minh tình trạng đơn' : 'Xem xét yêu cầu'}</strong><p>{draft.proposal}</p></div></div></section>
        {item && Boolean(item.next_statuses.length) && <form className="update" onSubmit={event=>{event.preventDefault(); onUpdate(item,next,note.trim());}}>
          <label>Trạng thái mới<select value={next} onChange={event=>setStatus(event.target.value)}>{item.next_statuses.map(choice=><option key={choice.value} value={choice.value}>{choice.label}</option>)}</select></label>
          <label>Phản hồi cho khách<textarea value={note} onChange={event=>setNote(event.target.value)} placeholder="Ví dụ: Đang đối chiếu thông tin giao hàng" maxLength={800} required/></label>
          <button className="primary" disabled={busy || !note.trim()}>Cập nhật ca</button>
        </form>}
        <section className="dossier-section"><h2>Tiến độ xử lý</h2><Progress status={item?.status}/></section>
      </>}
    </section>
    <aside className="rail"><OrderInfo order={order}/><section className="panel details"><h2>Lịch sử cập nhật</h2>
      {item?.events.length ? <ol className="activity">{item.events.map((event,index)=><li key={index}><strong>{event.actor === 'customer' ? 'Khách bổ sung' : labels[event.status]}</strong><p>{event.note}</p><small>{timestamp(event.at)}</small></li>)}</ol>
        : draft ? <ol className="activity">{order && <li><strong>Hệ thống ghi: {order.status}</strong><small>{timestamp(order.updated_at)}</small></li>}<li><strong>Hồ sơ nháp đã được chuẩn bị</strong><small>{timestamp(draft.created_at)}</small></li></ol> : <p className="muted">Chưa có cập nhật.</p>}
    </section></aside>
  </div>;
}

function App() {
  const [role, setRole] = useState<'customer'|'staff'>(()=>location.hash==='#nhan-vien' ? 'staff' : 'customer');
  const [customer, setCustomer] = useState<CustomerData | null>(null);
  const [staff, setStaff] = useState<StaffData | null>(null);
  const [selected, setSelected] = useState<number | null>(null);
  const [model, setModel] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  async function run(action: () => Promise<void>) {
    setBusy(true); setError('');
    try { await action(); }
    catch (failure) { setError(failure instanceof Error ? failure.message : 'Chưa xử lý được yêu cầu.'); }
    finally { setBusy(false); }
  }

  useEffect(()=>{ request<{provider:string;model:string}>('/health').then(info=>setModel(info.provider === 'ollama' ? `${info.model} · Local` : `${info.provider} · ${info.model}`)).catch(()=>setModel('Chưa kết nối')); }, []);
  useEffect(()=>{ void run(async()=>{
    if (role === 'customer') setCustomer(await request<CustomerData>('/customer'));
    else setStaff(await request<StaffData>('/staff'));
  }); }, [role]);

  function switchRole(value: 'customer'|'staff') {
    if (busy) return;
    location.hash = value === 'staff' ? 'nhan-vien' : 'khach-hang';
    setRole(value);
  }

  return <><header className="topbar"><div className="brand"><span><ChatTextIcon size={25} weight="bold"/></span>Ishowspeed</div>
    <nav aria-label="Chọn vai trò mô phỏng"><button aria-pressed={role==='customer'} disabled={busy} onClick={()=>switchRole('customer')}>Khách hàng</button><button aria-pressed={role==='staff'} disabled={busy} onClick={()=>switchRole('staff')}>Bàn nhân viên</button></nav>
    <div className="model" title="Dữ liệu mô phỏng"><UserCircleIcon size={25}/><small>{model || 'Đang kết nối'}</small></div></header>
    <main>
      {error && <div className="error" role="alert"><WarningCircleIcon size={21}/>{error}</div>}
      {role==='customer' ? <CustomerWorkspace data={customer} busy={busy}
        onSend={text=>void run(async()=>setCustomer(await request<CustomerData>('/customer/messages','POST',{text})))}
        onReset={()=>void run(async()=>setCustomer(await request<CustomerData>('/customer/reset','POST')))}
        onRefresh={()=>void run(async()=>setCustomer(await request<CustomerData>('/customer')))}/>
        : <StaffWorkspace data={staff} selected={selected} onSelect={setSelected} busy={busy}
          onReceive={()=>void run(async()=>{const item = await request<StaffCase>('/staff/receive','POST'); setSelected(item.id); setStaff(await request<StaffData>('/staff'));})}
          onUpdate={(item,status,note)=>void run(async()=>{await request<StaffCase>(`/staff/cases/${item.id}`,'PATCH',{version:item.version,status,note}); setStaff(await request<StaffData>('/staff'));})}/>}
    </main></>;
}

createRoot(document.getElementById('root')!).render(<App/>);
