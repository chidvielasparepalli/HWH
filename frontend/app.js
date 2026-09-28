const API="http://127.0.0.1:8000/api";
const $=id=>document.getElementById(id);
const status=t=>$("status").textContent="● "+t;
async function call(path,opts={}){const r=await fetch(API+path,{headers:{"Content-Type":"application/json"},...opts});const d=await r.json();if(!r.ok)throw Error(d.detail||"Request failed");return d}
$("saveBtn").onclick=async()=>{try{status("Saving memory...");await call("/interactions",{method:"POST",body:JSON.stringify({customer:$("customer").value,interaction:$("interaction").value})});$("interaction").value="";status("Memory retained")}catch(e){status(e.message)}};
$("seedBtn").onclick=async()=>{try{status("Loading demo experience...");const d=await call("/demo-seed");status(d.stored+" memories retained")}catch(e){status(e.message)}};
$("askBtn").onclick=async()=>{try{status("Recalling + reflecting...");const d=await call("/advice",{method:"POST",body:JSON.stringify({customer:$("adviceCustomer").value,query:$("query").value})});$("answer").textContent=d.answer;$("memory").textContent=JSON.stringify(d.memory,null,2);$("reflection").textContent=JSON.stringify(d.reflection,null,2);$("bank").textContent="Bank: "+d.bank_id;status("Learned from memory")}catch(e){status(e.message)}};
