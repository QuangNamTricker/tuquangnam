// ================================================================
// FACEBOOK COOKIE → TOKEN CONVERTER - Cloudflare Worker v2.0
// Author: Từ Quang Nam
// Zalo: 0888385536
// ================================================================

// ================================================================
// CẤU HÌNH
// ================================================================

const CONFIG = {
    APP_ID: '350685531728',
    ACCESS_TOKEN: '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
    API_KEY: '882a8490361da98702bf97a021ddc14d',
    SIG: '214049b9f17c38bd767de53752b53946',
    GRAPH_URL: 'https://graph.facebook.com'
};

// Danh sách ứng dụng để chuyển đổi token
const APP_LIST = {
    'FB_ANDROID': {
        name: 'Facebook For Android',
        app_id: '350685531728',
        prefix: 'EAAAAU'
    },
    'MESSENGER_ANDROID': {
        name: 'Messenger For Android',
        app_id: '256002347743983',
        prefix: 'EAAD'
    },
    'FB_LITE': {
        name: 'Facebook Lite',
        app_id: '275254692598279',
        prefix: 'EAAD6V7'
    },
    'MESSENGER_LITE': {
        name: 'Messenger Lite',
        app_id: '200424423651082',
        prefix: 'EAAC2S'
    },
    'ADS_MANAGER_ANDROID': {
        name: 'Ads Manager Android',
        app_id: '438142079694454',
        prefix: 'EAAGO'
    },
    'PAGES_MANAGER_ANDROID': {
        name: 'Pages Manager Android',
        app_id: '121876164619130',
        prefix: 'EAAB'
    },
    'FB_IPHONE': {
        name: 'Facebook For iPhone',
        app_id: '6628568379',
        prefix: 'EAAAAA'
    },
    'MESSENGER_IPHONE': {
        name: 'Messenger For iPhone',
        app_id: '237759909591655',
        prefix: 'EAADYP'
    }
};

// ================================================================
// HÀM XỬ LÝ COOKIES
// ================================================================

function parseCookies(cookieString) {
    const clean = cookieString.trim();
    const pairs = clean.split(/;\s*/);
    const cookieMap = {};

    for (const pair of pairs) {
        if (!pair) continue;
        const sepIndex = pair.indexOf('=');
        if (sepIndex === -1) continue;
        const key = pair.substring(0, sepIndex).trim();
        const value = pair.substring(sepIndex + 1).trim();
        if (key && value) {
            cookieMap[key] = value;
        }
    }
    return cookieMap;
}

function validateCookies(cookieMap) {
    const c_user = cookieMap['c_user'];
    const xs = cookieMap['xs'];

    if (!c_user) {
        return { valid: false, message: 'Thiếu cookie c_user (User ID)' };
    }
    if (!xs) {
        return { valid: false, message: 'Thiếu cookie xs (Session token)' };
    }
    if (!/^\d+$/.test(c_user)) {
        return { valid: false, message: 'c_user không hợp lệ (phải là số)' };
    }
    if (xs.length < 5) {
        return { valid: false, message: 'xs quá ngắn, không hợp lệ' };
    }

    return { valid: true, message: 'Cookies hợp lệ' };
}

function extractCookieInfo(cookieMap) {
    return {
        c_user: cookieMap['c_user'] || null,
        xs: cookieMap['xs'] || null,
        fr: cookieMap['fr'] || null,
        datr: cookieMap['datr'] || null,
        sb: cookieMap['sb'] || null
    };
}

// ================================================================
// TẠO TOKEN TỪ COOKIES
// ================================================================

function generateTokenFromCookies(cookieMap) {
    const c_user = cookieMap['c_user'] || '';
    const xs = cookieMap['xs'] || '';
    const fr = cookieMap['fr'] || '';
    const datr = cookieMap['datr'] || '';
    const sb = cookieMap['sb'] || '';

    const timestamp = Date.now();

    // Dữ liệu để mã hóa - giống với cách Python
    const dataToEncode = JSON.stringify({
        uid: c_user,
        xs: xs.substring(0, 30),
        fr: fr ? fr.substring(0, 20) : '',
        datr: datr ? datr.substring(0, 10) : '',
        sb: sb ? sb.substring(0, 10) : '',
        ts: timestamp,
        app_id: CONFIG.APP_ID
    });

    // Encode base64 URL-safe
    let encoded = btoa(unescape(encodeURIComponent(dataToEncode)));
    encoded = encoded.replace(/=/g, '')
        .replace(/\+/g, '-')
        .replace(/\//g, '_');

    return 'EAAAAU' + encoded;
}

// ================================================================
// LẤY THÔNG TIN NGƯỜI DÙNG TỪ TOKEN
// ================================================================

async function getUserInfo(accessToken) {
    try {
        const response = await fetch(`${CONFIG.GRAPH_URL}/me?access_token=${accessToken}`);
        const data = await response.json();
        if (data.id) {
            return {
                success: true,
                name: data.name || 'Unknown',
                id: data.id,
                email: data.email || null
            };
        }
        return { 
            success: false, 
            error: data.error?.message || 'Không thể lấy thông tin',
            data: data
        };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// ================================================================
// CHUYỂN ĐỔI TOKEN SANG ỨNG DỤNG KHÁC
// ================================================================

async function convertToken(accessToken, targetApp) {
    try {
        const appId = targetApp.app_id;
        
        // Tạo form data
        const formData = new URLSearchParams();
        formData.append('access_token', accessToken);
        formData.append('format', 'json');
        formData.append('new_app_id', appId);
        formData.append('generate_session_cookies', '1');

        const response = await fetch('https://api.facebook.com/method/auth.getSessionforApp', {
            method: 'POST',
            headers: {
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; Redmi Note 8 Build/PQ3A.190705.08211809) [FBAN/FB4A;FBAV/417.0.0.33.65;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/480086274;FBCR/MobiFone;FBMF/Redmi;FBBD/Redmi;FBDV/Redmi Note 8;FBSV/9;FBCA/x86:armeabi-v7a;FBDM/{density=1.5,width=1280,height=720};FB_FW/1;FBRV/0;]',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData.toString()
        });

        const data = await response.json();

        if (data.access_token) {
            return {
                success: true,
                access_token: data.access_token,
                prefix: extractPrefix(data.access_token),
                cookies: data.session_cookies || []
            };
        }

        return {
            success: false,
            error: data.error?.message || 'Không thể chuyển đổi token'
        };

    } catch (error) {
        return {
            success: false,
            error: error.message || 'Network error'
        };
    }
}

function extractPrefix(token) {
    if (!token) return 'UNKNOWN';
    for (let i = 0; i < token.length; i++) {
        if (token[i] >= 'a' && token[i] <= 'z') {
            return token.substring(0, i);
        }
    }
    return token.substring(0, 10);
}

// ================================================================
// XỬ LÝ REQUEST
// ================================================================

async function handleRequest(request) {
    // CORS headers
    const corsHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    };

    if (request.method === 'OPTIONS') {
        return new Response(null, { headers: corsHeaders });
    }

    const url = new URL(request.url);

    // ============================================================
    // GET: Lấy thông tin từ token hoặc cookies
    // ============================================================
    if (request.method === 'GET') {
        const token = url.searchParams.get('token');
        const cookies = url.searchParams.get('cookies');

        if (token) {
            const info = await getUserInfo(token);
            if (info.success) {
                return new Response(JSON.stringify({
                    success: true,
                    token: token,
                    prefix: extractPrefix(token),
                    name: info.name,
                    id: info.id,
                    email: info.email
                }), { headers: corsHeaders });
            }
            return new Response(JSON.stringify({
                success: false,
                error: info.error || 'Token không hợp lệ'
            }), { status: 400, headers: corsHeaders });
        }

        if (cookies) {
            return await convertCookiesToToken(cookies, corsHeaders);
        }

        return new Response(JSON.stringify({
            success: false,
            error: 'Thiếu tham số token hoặc cookies',
            usage: {
                token: '/?token=YOUR_TOKEN',
                cookies: '/?cookies=YOUR_COOKIES_STRING'
            }
        }), { status: 400, headers: corsHeaders });
    }

    // ============================================================
    // POST: Chuyển đổi cookies → token
    // ============================================================
    if (request.method === 'POST') {
        try {
            const body = await request.json();
            const cookies = body.cookies;

            if (!cookies) {
                return new Response(JSON.stringify({
                    success: false,
                    error: 'Thiếu cookies trong body'
                }), { status: 400, headers: corsHeaders });
            }

            return await convertCookiesToToken(cookies, corsHeaders);
        } catch (error) {
            return new Response(JSON.stringify({
                success: false,
                error: error.message || 'Invalid request body'
            }), { status: 400, headers: corsHeaders });
        }
    }

    return new Response('Method not allowed', { status: 405, headers: corsHeaders });
}

// ================================================================
// CHUYỂN ĐỔI COOKIES → TOKEN (HÀM CHÍNH)
// ================================================================

async function convertCookiesToToken(cookiesString, corsHeaders) {
    const cookieMap = parseCookies(cookiesString);

    // Validate cookies
    const validation = validateCookies(cookieMap);
    if (!validation.valid) {
        return new Response(JSON.stringify({
            success: false,
            error: validation.message,
            cookies: cookieMap
        }), { status: 400, headers: corsHeaders });
    }

    try {
        // 1. Tạo token từ cookies
        const token = generateTokenFromCookies(cookieMap);
        const prefix = extractPrefix(token);
        const c_user = cookieMap['c_user'] || '';

        // 2. Lấy thông tin user từ token
        const userInfo = await getUserInfo(token);
        const name = userInfo.success ? userInfo.name : 'Unknown';

        // 3. Build cookies string
        const cookiesStringResult = Object.entries(cookieMap)
            .map(([k, v]) => `${k}=${v}`)
            .join('; ');

        // 4. Chuyển đổi sang các app khác
        const convertedTokens = {};
        const appKeys = Object.keys(APP_LIST);

        for (const key of appKeys) {
            if (key === 'FB_ANDROID') continue;
            
            const app = APP_LIST[key];
            const result = await convertToken(token, app);
            
            if (result.success) {
                convertedTokens[key] = {
                    name: app.name,
                    prefix: result.prefix,
                    token: result.access_token,
                    success: true
                };
            } else {
                convertedTokens[key] = {
                    name: app.name,
                    success: false,
                    error: result.error || 'Failed'
                };
            }
        }

        // 5. Kết quả cuối cùng
        const result = {
            success: true,
            name: name,
            uid: c_user,
            cookies: {
                string: cookiesStringResult,
                dict: cookieMap
            },
            original_token: {
                prefix: prefix,
                token: token
            },
            converted_tokens: convertedTokens,
            timestamp: new Date().toISOString()
        };

        return new Response(JSON.stringify(result), { headers: corsHeaders });

    } catch (error) {
        return new Response(JSON.stringify({
            success: false,
            error: error.message || 'Lỗi khi xử lý cookies',
            cookies: cookieMap
        }), { status: 500, headers: corsHeaders });
    }
}

// ================================================================
// REGISTER WORKER
// ================================================================

addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request));
});