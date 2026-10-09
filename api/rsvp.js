export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    let body = req.body;
    if (typeof body === 'string') {
      try {
        body = JSON.parse(body);
      } catch (e) {
        return res.status(400).json({ error: 'Invalid JSON payload' });
      }
    } else if (!body && req.on) {
      const raw = await new Promise((resolve, reject) => {
        let data = '';
        req.on('data', chunk => { data += chunk; });
        req.on('end', () => resolve(data));
        req.on('error', reject);
      });
      if (raw) {
        try {
          body = JSON.parse(raw);
        } catch (e) {
          return res.status(400).json({ error: 'Invalid JSON payload' });
        }
      }
    }

    const { fullName, whatsapp, attending, message } = body || {};

    if (!fullName || typeof fullName !== 'string' || !fullName.trim()) {
      return res.status(400).json({ error: 'Full name is required.' });
    }

    let attendingStatus = 'Joyfully Accept';
    if (attending === 'Regretfully Decline' || attending === 'no') {
      attendingStatus = 'Regretfully Decline';
    } else if (attending === 'Joyfully Accept' || attending === 'yes') {
      attendingStatus = 'Joyfully Accept';
    } else if (attending && typeof attending === 'string') {
      attendingStatus = attending.trim();
    }

    const NOTION_API_KEY = process.env.NOTION_API_KEY;
    const NOTION_DATABASE_ID = process.env.NOTION_DATABASE_ID;

    if (!NOTION_API_KEY || !NOTION_DATABASE_ID) {
      console.error('Missing NOTION_API_KEY or NOTION_DATABASE_ID');
      return res.status(500).json({ error: 'Server configuration error: Notion credentials missing.' });
    }

    const notionPayload = {
      parent: { database_id: NOTION_DATABASE_ID },
      properties: {
        'Full Name': {
          title: [
            {
              text: {
                content: fullName.trim()
              }
            }
          ]
        },
        ...(whatsapp && typeof whatsapp === 'string' && whatsapp.trim()
          ? {
              'WhatsApp Number': {
                phone_number: whatsapp.trim()
              }
            }
          : {}),
        'Attending': {
          select: {
            name: attendingStatus
          }
        },
        'Message for the Couple': {
          rich_text:
            message && typeof message === 'string' && message.trim()
              ? [
                  {
                    text: {
                      content: message.trim()
                    }
                  }
                ]
              : []
        }
      }
    };

    const notionRes = await fetch('https://api.notion.com/v1/pages', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${NOTION_API_KEY}`,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(notionPayload)
    });

    const notionData = await notionRes.json();

    if (!notionRes.ok) {
      console.error('Notion API error:', notionData);
      return res.status(502).json({
        error: notionData.message || 'Error creating RSVP record in Notion.'
      });
    }

    return res.status(200).json({
      success: true,
      pageId: notionData.id
    });
  } catch (error) {
    console.error('RSVP Serverless Function Error:', error);
    return res.status(500).json({
      error: error.message || 'Internal Server Error'
    });
  }
}
