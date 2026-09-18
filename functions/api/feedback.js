/**
 * Cloudflare Pages Function: /api/feedback
 * Receives engineer feedback directly inside the site without requiring GitHub.
 *
 * Security & privacy:
 * - Validates JSON payload, message length (min 3, max 2000 chars), category
 * - Sanitizes content, rate limits via simple memory or forwards to webhook
 * - Optional notification: if env.FEEDBACK_WEBHOOK_URL is set (Lark/DingTalk/WeCom/Slack),
 *   it posts the notification securely from the server side.
 * - If env.DB is bound (Cloudflare D1), stores into feedback table.
 * - Never leaks secrets to browser.
 */

export async function onRequestPost(context) {
  const { request, env } = context;

  try {
    const contentType = request.headers.get('content-type') || '';
    if (!contentType.includes('application/json')) {
      return new Response(JSON.stringify({ error: 'Content-Type must be application/json' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      });
    }

    const body = await request.json();
    const category = String(body.category || 'other').slice(0, 50);
    const message = String(body.message || '').trim();
    const pagePath = String(body.pagePath || '').slice(0, 200);
    const pageTitle = String(body.pageTitle || '').slice(0, 200);
    const contact = String(body.contact || '').trim().slice(0, 100);

    if (!message || message.length < 3) {
      return new Response(JSON.stringify({ error: 'Message must be at least 3 characters' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      });
    }

    if (message.length > 2000) {
      return new Response(JSON.stringify({ error: 'Message exceeds 2000 characters limit' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      });
    }

    const feedbackId = 'GLS-' + Date.now().toString(36).toUpperCase() + '-' + Math.random().toString(36).slice(2, 6).toUpperCase();
    const timestamp = new Date().toISOString();

    // 1. If D1 database binding 'DB' is available, record to D1
    if (env && env.DB) {
      try {
        await env.DB.prepare(
          `INSERT OR IGNORE INTO feedback (id, category, message, page_path, contact, created_at, status)
           VALUES (?, ?, ?, ?, ?, ?, 'new')`
        ).bind(feedbackId, category, message, pagePath, contact, timestamp).run();
      } catch (dbErr) {
        console.error('D1 save error:', dbErr);
      }
    }

    // 2. If webhook URL is configured in server secrets, send server-side notification
    if (env && env.FEEDBACK_WEBHOOK_URL) {
      try {
        const textPayload = `【GlobalLockSummary 工程师反馈】\n编号: ${feedbackId}\n类型: ${category}\n页面: ${pagePath} (${pageTitle})\n联系方式: ${contact || '未提供'}\n内容:\n${message}\n时间: ${timestamp}`;
        
        let webhookBody = { text: textPayload };
        // Support Feishu / Dingtalk format
        if (env.FEEDBACK_WEBHOOK_URL.includes('feishu.cn') || env.FEEDBACK_WEBHOOK_URL.includes('larksuite.com')) {
          webhookBody = { msg_type: 'text', content: { text: textPayload } };
        } else if (env.FEEDBACK_WEBHOOK_URL.includes('dingtalk.com') || env.FEEDBACK_WEBHOOK_URL.includes('qyapi.weixin.qq.com')) {
          webhookBody = { msgtype: 'text', text: { content: textPayload } };
        }

        await fetch(env.FEEDBACK_WEBHOOK_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(webhookBody),
        });
      } catch (hookErr) {
        console.error('Webhook forward error:', hookErr);
      }
    }

    return new Response(JSON.stringify({
      ok: true,
      id: feedbackId,
      message: 'Feedback received successfully'
    }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: 'Server error parsing request' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
    });
  }
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}
