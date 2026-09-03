// Vercel Edge Function: POST /api/lead
// Windows Roofs Plus — estimate request handler.
//
// Current mode: notification only (no CRM).
//   Set ONE of these env vars in the Vercel project:
//     FORMSPREE_ID   e.g. "xabcdefg"   -> posts to https://formspree.io/f/<id>
//     LEAD_WEBHOOK   full https URL     -> posts the JSON payload as-is
//   If neither is set the endpoint returns 503 and the form tells the caller to phone in.
//
// To add GoHighLevel later: fill in the sendToGHL() block at the bottom and
// call it before the notification step. Nothing else needs to change.

export const config = { runtime: 'edge' };

const PHONE = '(954) 706-8028';

function json(body, status = 200, origin = '*') {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Cache-Control': 'no-store',
    },
  });
}

async function parseBody(req) {
  const ct = req.headers.get('content-type') || '';
  if (ct.includes('application/json')) return req.json();
  return Object.fromEntries(new URLSearchParams(await req.text()));
}

export default async function handler(req) {
  if (req.method === 'OPTIONS') return new Response(null, { status: 204 });
  if (req.method !== 'POST') return json({ ok: false, error: 'method_not_allowed' }, 405);

  const origin = req.headers.get('origin') || 'https://windowsroofsplus.com';

  let data;
  try {
    data = await parseBody(req);
  } catch (_) {
    return json({ ok: false, error: 'invalid_request', message: 'We could not read that request' }, 400, origin);
  }

  // honeypot — silently accept, never notify
  if (data._gotcha) return json({ ok: true, receipt: { skipped: true } }, 201, origin);

  const name    = String(data.name || '').trim();
  const email   = String(data.email || '').trim();
  const phone   = String(data.phone || '').trim();
  const city    = String(data.city || '').trim();
  const service = String(data.service || 'Estimate request').trim();
  const details = String(data.details || '').trim();

  if (!name || (!email && !phone)) {
    return json(
      { ok: false, error: 'missing_contact_details', message: 'Enter your name and a phone number or email' },
      422, origin
    );
  }

  const lead = {
    name, email, phone, city, service, details,
    page_url: String(data.page_url || ''),
    submitted_at: new Date().toISOString(),
    _subject: `WRP estimate request — ${service}${city ? ' · ' + city : ''} — ${name}`,
  };

  const formspreeId = process.env.FORMSPREE_ID;
  const webhook = process.env.LEAD_WEBHOOK;

  if (!formspreeId && !webhook) {
    return json(
      { ok: false, error: 'notify_unconfigured', message: `Online requests are temporarily unavailable. Please call ${PHONE}` },
      503, origin
    );
  }

  try {
    let delivered = false;

    if (formspreeId) {
      const r = await fetch(`https://formspree.io/f/${formspreeId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(lead),
      });
      delivered = r.ok;
    }

    if (!delivered && webhook) {
      const r = await fetch(webhook, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(lead),
      });
      delivered = r.ok;
    }

    if (!delivered) throw new Error('Notification endpoint rejected the request');

    return json({ ok: true, receipt: { delivered: true, submitted_at: lead.submitted_at } }, 201, origin);
  } catch (error) {
    console.error('WRP lead delivery failed:', error?.message);
    return json(
      { ok: false, error: 'delivery_failed', message: `We could not save your request. Please call ${PHONE}` },
      502, origin
    );
  }
}

/* ------------------------------------------------------------------
   GHL hook-up (currently unused — wire when the sub-account exists).

   async function sendToGHL(lead) {
     const token      = process.env.GHL_WRP_LOCATION_PIT;
     const locationId = process.env.GHL_WRP_LOCATION_ID;
     const pipelineId = process.env.GHL_WRP_PIPELINE_ID;
     if (!token || !locationId || !pipelineId) return null;

     const post = (path, body) => fetch(`https://services.leadconnectorhq.com${path}`, {
       method: 'POST',
       headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}`, Version: '2021-07-28' },
       body: JSON.stringify(body),
     }).then(r => r.json());

     const contact = await post('/contacts/upsert', {
       locationId,
       firstName: lead.name.split(/\s+/)[0],
       lastName: lead.name.split(/\s+/).slice(1).join(' '),
       phone: lead.phone, email: lead.email,
       source: 'windowsroofsplus.com',
       tags: ['wrp-website', `service:${lead.service}`, lead.city ? `city:${lead.city}` : null].filter(Boolean),
     });
     const contactId = contact?.contact?.id || contact?.id;

     const opp = await post('/opportunities/', {
       locationId, pipelineId, contactId, status: 'open',
       name: `${lead.service} - ${lead.name}`,
       source: 'windowsroofsplus.com',
     });
     return { contactId, opportunityId: opp?.opportunity?.id || opp?.id };
   }
------------------------------------------------------------------ */
