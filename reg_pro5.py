from pystyle import Colors, Colorate
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
import requests, os, random, json, time
from datetime import datetime
from time import sleep
from typing import Optional, Tuple, Dict, List
import socket

# =========================== [ PAGE CONTENT GENERATOR ] ===========================
class PageContentGenerator:
    def __init__(self):
        self.bios = [
            "Chào mừng đến với {page_name}! Chúng tôi cung cấp {service} chất lượng cao.",
            "Xin chào! {page_name} - Nơi chia sẻ {topic} và {interest}.",
            "Chào bạn! {page_name} chuyên về {service} và {topic} hàng đầu.",
            "{page_name} - {service} uy tín, {topic} đột phá.",
            "Kết nối cùng {page_name} để nhận {service} và {topic} mới nhất.",
            "{page_name} - Nơi {interest} và {topic} gặp gỡ.",
            "Chào mừng đến với {page_name}! Chúng tôi mang đến {service} {topic}.",
            "Hãy khám phá {page_name} - {service} và {topic} dành cho bạn."
        ]
        
        self.services = ["sản phẩm", "dịch vụ", "giải pháp", "tư vấn", 
                        "nội dung", "kiến thức", "trải nghiệm", "cộng đồng"]
        self.topics = ["kiến thức", "trải nghiệm", "cảm hứng", "sáng tạo",
                      "phát triển", "kết nối", "chia sẻ", "học hỏi"]
        self.interests = ["cộng đồng", "phát triển", "kết nối", "khám phá",
                         "sáng tạo", "đam mê", "năng lượng", "tích cực"]
        self.visions = ["top 1", "số 1", "hàng đầu", "tiên phong", "dẫn đầu"]
        self.values = ["giá trị", "sự khác biệt", "thay đổi tích cực", 
                      "niềm tin", "phát triển bền vững"]
        
        # Danh sách tên page tiếng Việt
        self.vietnamese_page_names = [
            "Thế Giới {topic}",
            "Cộng Đồng {topic} {service}",
            "{topic} Việt Nam",
            "{service} {topic} 24/7",
            "Chia Sẻ {topic}",
            "Học {topic} Cùng Nhau",
            "Khám Phá {topic} Mới",
            "Phát Triển {topic} Toàn Diện"
        ]
        
    def generate_vietnamese_page_name(self) -> str:
        """Tạo tên page tiếng Việt ngẫu nhiên"""
        template = random.choice(self.vietnamese_page_names)
        return template.format(
            topic=random.choice(self.topics),
            service=random.choice(self.services)
        )
    
    def generate_bio(self, page_name: str) -> str:
        """Tạo bio tự động cho page"""
        template = random.choice(self.bios)
        return template.format(
            page_name=page_name,
            service=random.choice(self.services),
            topic=random.choice(self.topics),
            interest=random.choice(self.interests)
        )
    
    def generate_about(self, page_name: str) -> str:
        """Tạo phần giới thiệu chi tiết"""
        service = random.choice(self.services)
        topic = random.choice(self.topics)
        vision = random.choice(self.visions)
        value = random.choice(self.values)
        
        return f"""📌 {page_name} - {service.upper()}
        
🌟 Sứ mệnh: Mang đến {topic} tốt nhất cho cộng đồng.
💡 Tầm nhìn: Trở thành {vision} trong lĩnh vực {service}.
🤝 Kết nối: Hãy cùng chúng tôi tạo nên {value}.
📊 Cam kết: Chất lượng - Uy tín - Chuyên nghiệp
🚀 Định hướng: Phát triển bền vững và không ngừng đổi mới"""
    
    def generate_page_username(self, page_name: str) -> str:
        """Tạo username cho page"""
        # Loại bỏ dấu tiếng Việt
        vietnamese_chars = {
            'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
            'ă': 'a', 'ắ': 'a', 'ằ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
            'â': 'a', 'ấ': 'a', 'ầ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
            'đ': 'd', 'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
            'ê': 'e', 'ế': 'e', 'ề': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
            'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
            'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
            'ô': 'o', 'ố': 'o', 'ồ': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
            'ơ': 'o', 'ớ': 'o', 'ờ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
            'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
            'ư': 'u', 'ứ': 'u', 'ừ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
            'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y'
        }
        
        # Chuyển đổi và làm sạch tên
        name_clean = ''
        for c in page_name:
            if c in vietnamese_chars:
                name_clean += vietnamese_chars[c]
            elif c.isalnum() or c.isspace():
                name_clean += c.lower()
        
        # Chỉ giữ lại chữ và số
        name_clean = ''.join(e for e in name_clean if e.isalnum())
        
        suffixes = ['', 'official', 'vn', 'page', 'real', 'community', 'group', 'hub', 'center']
        suffix = random.choice(suffixes)
        
        if suffix:
            return f"{name_clean}{suffix}"
        else:
            # Nếu không có suffix, thêm số ngẫu nhiên nếu tên quá ngắn
            if len(name_clean) < 3:
                return f"{name_clean}{random.randint(10, 99)}"
            return name_clean

# =========================== [ MAIN TOOL CLASS ] ===========================
class API_PRO5_ByTừQuangNam:
    def __init__(self):
        self.console = Console()
        self.content_generator = PageContentGenerator()
        self.list_clone = []
        self.dem = 0
        self.stt = 0
        self.slpage = 0
        self.created_pages = []
        
    def banner(self):
        os.system('title TOOL REG PAGE PRO5 | ĐA LUỒNG - TỪ QUANG NAM')
        os.system("cls" if os.name == "nt" else "clear")
        
        banner_ascii = """
╔════════════════════════════════════════════════════════════════╗
║           𝓟𝓡𝓞𝓕𝓘𝓛𝓔 𝓒𝓡𝓔𝓐𝓣𝓞𝓡 𝓟𝓡𝓞 𝓥5 - 𝓑𝓨 𝓣𝓤 𝓠𝓤𝓐𝓝𝓖 𝓝𝓐𝓜           ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"""
        
        colored_banner = Colorate.Diagonal(Colors.blue_to_purple, banner_ascii)
        print(colored_banner)
        
        info_text = Text()
        info_text.append("Version: ", style="bold cyan")
        info_text.append("PRO5 v3.0 ", style="bold yellow")
        info_text.append("| ", style="white")
        info_text.append("Developer: ", style="bold cyan")
        info_text.append("TỪ QUANG NAM", style="bold green")
        info_text.append(" | ", style="white")
        info_text.append("Date: ", style="bold cyan")
        info_text.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), style="bold white")
        
        info_panel = Panel(info_text, style="bright_magenta", width=80)
        self.console.print(info_panel)
    
    def show_stats(self):
        """Hiển thị thống kê real-time"""
        table = Table(show_header=True, header_style="bold magenta", width=80)
        table.add_column("📊 THỐNG KÊ", style="cyan", width=40)
        table.add_column("🔢 SỐ LƯỢNG", style="green", justify="center", width=40)
        
        table.add_row("Cookie hợp lệ", f"[bold yellow]{len(self.list_clone)}[/bold yellow]")
        table.add_row("Page đã tạo", f"[bold green]{self.dem}[/bold green]")
        table.add_row("Mục tiêu", f"[bold cyan]{self.slpage}[/bold cyan]")
        
        self.console.print(table)
    
    def save_to_json(self, page_data: Dict):
        """Lưu thông tin page vào file JSON (append mode)"""
        try:
            filename = f"created_pages_{datetime.now().strftime('%d%m%Y')}.json"
            
            # Đọc dữ liệu cũ nếu có
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            else:
                existing_data = []
            
            # Thêm dữ liệu mới vào đầu list
            existing_data.insert(0, page_data)
            
            # Giới hạn số lượng bản ghi (tối đa 1000 bản ghi)
            if len(existing_data) > 1000:
                existing_data = existing_data[:1000]
            
            # Lưu file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            self.console.print(f'\033[0;31mLỗi khi lưu JSON: {e}')
            return False
    
    def create_page_info(self, name_fb: str, uid_fb: str, page_name: str, 
                         page_id: str, page_username: str, bio: str, about: str):
        """Tạo dictionary chứa thông tin page"""
        return {
            "facebook_account": {
                "name": name_fb,
                "uid": uid_fb
            },
            "created_page": {
                "page_id": page_id,
                "page_name": page_name,
                "page_username": page_username,
                "bio": bio,
                "about": about,
                "creation_time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "timestamp": datetime.now().isoformat()
            },
            "tool_info": {
                "tool_name": "PRO5 Profile Creator",
                "version": "3.0",
                "developer": "TỪ QUANG NAM"
            }
        }
    
    def tqn_delay_tool(self, p: int):
        """Hiển thị loading animation với countdown"""
        with self.console.status(f"[bold blue]⏳ Đang chờ {p} giây...") as status:
            for i in range(p, 0, -1):
                status.update(status=f"[bold blue]⏳ Đang chờ {i} giây...")
                sleep(1)
    
    def check_network(self) -> bool:
        """Kiểm tra kết nối mạng bằng cách ping Facebook"""
        try:
            # Thử kết nối đến Facebook
            response = requests.get('https://www.facebook.com', timeout=5)
            return response.status_code == 200
        except:
            # Thử cách khác nếu request thất bại
            try:
                socket.gethostbyname('www.facebook.com')
                return True
            except:
                return False
    
    def getthongtinfacebook(self, cookie: str) -> Optional[Tuple]:
        headers_get = {
            'authority': 'www.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'viewport-width': '1184',
            'cookie': cookie
        }
        
        try:
            url_profile = requests.get('https://www.facebook.com/me', headers=headers_get, timeout=30).url
            get_dulieu_profile = requests.get(url=url_profile, headers=headers_get, timeout=30).text
        except Exception as e:
            self.console.print(f'❌ Lỗi khi lấy thông tin: {e}')
            return None
        
        try:
            uid_get = cookie.split('c_user=')[1].split(';')[0]
            fb_dtsg_get = get_dulieu_profile.split('{"name":"fb_dtsg","value":"')[1].split('"},')[0]
            jazoest_get = get_dulieu_profile.split('{"name":"jazoest","value":"')[1].split('"},')[0]
            name_get = get_dulieu_profile.split('<title>')[1].split('</title>')[0]
            return name_get, uid_get, fb_dtsg_get, jazoest_get
        except:
            try:
                uid_get = cookie.split('c_user=')[1].split(';')[0]
                fb_dtsg_get = get_dulieu_profile.split(',"f":"')[1].split('","l":null}')[0]
                jazoest_get = get_dulieu_profile.split('&jazoest=')[1].split('","e":"')[0]
                name_get = get_dulieu_profile.split('<title>')[1].split('</title>')[0]
                return name_get, uid_get, fb_dtsg_get, jazoest_get
            except:
                return None
    
    def generate_vietnamese_name(self) -> str:
        """Tạo tên tiếng Việt ngẫu nhiên"""
        first_names = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương"]
        middle_names = ["Văn", "Thị", "Hữu", "Công", "Minh", "Quốc", "Đức", "Anh", "Tuấn", "Hải", "Thanh", "Xuân", "Bá", "Gia", "Kim"]
        last_names = ["An", "Bình", "Cường", "Dũng", "Giang", "Hạnh", "Khang", "Long", "Nam", "Phúc", "Quân", "Sơn", "Thắng", "Vinh", "Yến"]
        
        return f"{random.choice(first_names)} {random.choice(middle_names)} {random.choice(last_names)}"
    
    def RegPage(self, cookie: str, name: str, uid: str, fb_dtsg: str, jazoest: str) -> Tuple[bool, str, str]:
        """
        Tạo page Facebook
        Returns: (success, page_id, page_name)
        """
        # Kiểm tra kết nối mạng
        if not self.check_network():
            self.console.print("❌ LỖI MẠNG: Không thể kết nối đến Facebook")
            return False, "", ""
        
        # Tạo tên page từ content generator
        page_name = self.content_generator.generate_vietnamese_page_name()
        page_username = self.content_generator.generate_page_username(page_name)
        bio = self.content_generator.generate_bio(page_name)
        about = self.content_generator.generate_about(page_name)
        
        headers_reg = {
            'authority': 'www.facebook.com',
            'accept': '*/*',
            'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
            'origin': 'https://www.facebook.com',
            'referer': 'https://www.facebook.com/pages/creation?ref_type=launch_point',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'viewport-width': '979',
            'x-fb-friendly-name': 'AdditionalProfilePlusCreationMutation',
            'x-fb-lsd': 'ZM7FAk6cuRcUp3imwqvHTY',
            'cookie': cookie
        }
        
        data_reg = {
            'av': uid,
            '__user': uid,
            '__a': '1',
            '__dyn': '7AzHxq1mxu1syUbFuC0BVU98nwgU29zEdEc8co5S3O2S7o11Ue8hw6vwb-q7oc81xoswIwuo886C11xmfz81sbzoaEnxO0Bo7O2l2Utwwwi831wiEjwZwlo5qfK6E7e58jwGzE8FU5e7oqBwJK2W5olwuEjUlDw-wUws9ovUaU3qxWm2Sq2-azo2NwkQ0z8c84K2e3u362-2B0oobo',
            '__csr': 'gP4ZAN2d-hbbRmLObkZO8LvRcXWVvth9d9GGXKSiLCqqr9qEzGTozAXiCgyBhbHrRG8VkQm8GFAfy94bJ7xeufz8jK8yGVVEgx-7oiwxypqCwgF88rzKV8y2O4ocUak4UpDxu3x1K4opAUrwGx63J0Lw-wa90eG18wkE7y14w4hw6Bw2-o069W00CSE0PW06aU02Z3wjU6i0btw3TE1wE5u',
            '__req': 't',
            '__hs': '19296.HYP:comet_pkg.2.1.0.2.1',
            'dpr': '1',
            '__ccg': 'EXCELLENT',
            '__rev': '1006496476',
            '__s': '1gapab:y4xv3f:2hb4os',
            '__hsi': '7160573037096492689',
            '__comet_req': '15',
            'fb_dtsg': fb_dtsg,
            'jazoest': jazoest,
            'lsd': 'ZM7FAk6cuRcUp3imwqvHTY',
            '__aaid': '800444344545377',
            '__spin_r': '1006496476',
            '__spin_b': 'trunk',
            '__spin_t': '1667200829',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'AdditionalProfilePlusCreationMutation',
            'variables': f'{{"input":{{"bio":"{bio}","categories":["181475575221097"],"creation_source":"comet","name":"{page_name}","page_referrer":"launch_point","actor_id":"{uid}","client_mutation_id":"1"}}}}',
            'server_timestamps': 'true',
            'doc_id': '5903223909690825',
        }
        
        try:
            # Tăng timeout và thêm retry
            session = requests.Session()
            session.timeout = 60
            
            response = session.post(
                'https://www.facebook.com/api/graphql/',
                headers=headers_reg,
                data=data_reg,
                timeout=60
            )
            
            # Kiểm tra response
            if response.status_code != 200:
                self.console.print(f"❌ HTTP Error {response.status_code}")
                return False, "", ""
            
            # Parse JSON an toàn
            try:
                response_data = response.json()
            except:
                self.console.print("❌ Không thể parse JSON response")
                return False, "", ""
            
            # Kiểm tra dữ liệu trả về
            if not response_data or 'data' not in response_data:
                self.console.print("❌ Response không có dữ liệu")
                return False, "", ""
            
            if 'additional_profile_plus_create' not in response_data['data']:
                self.console.print("❌ Không tìm thấy thông tin page trong response")
                return False, "", ""
            
            page_id = response_data['data']['additional_profile_plus_create']['additional_profile']['id']
            self.dem += 1
            
            # Hiển thị thông báo thành công
            success_text = Text()
            success_text.append(f"✅ {self.dem}", style="bold green")
            success_text.append(" | THÀNH CÔNG | ", style="white")
            success_text.append("FB: ", style="cyan")
            success_text.append(f"{name}", style="yellow")
            success_text.append(" | PAGE ID: ", style="cyan")
            success_text.append(f"{page_id}", style="bold red")
            success_text.append(" | TÊN PAGE: ", style="cyan")
            success_text.append(f"{page_name}", style="bold green")
            
            self.console.print(success_text)
            
            # Lưu thông tin page
            page_info = self.create_page_info(
                name, uid, page_name, page_id, page_username, bio, about
            )
            self.save_to_json(page_info)
            
            return True, page_id, page_name
            
        except requests.exceptions.Timeout:
            self.console.print("❌ LỖI: Timeout - Kết nối quá chậm")
            return False, "", ""
        except requests.exceptions.ConnectionError:
            self.console.print("❌ LỖI: Không thể kết nối - Kiểm tra mạng hoặc DNS")
            return False, "", ""
        except Exception as e:
            self.console.print(f"❌ LỖI: {str(e)}")
            return False, "", ""

    def validate_cookie(self, cookie: str) -> bool:
        """Validate cookie có hợp lệ không"""
        if not cookie or 'c_user' not in cookie:
            return False
        return True

# =========================== [ MAIN FUNCTION ] ===========================
def main():
    tqntool = API_PRO5_ByTừQuangNam()
    tqntool.banner()
    
    console = Console()
    
    # Panel hướng dẫn
    guide_panel = Panel(
        "📝 [bold cyan]HƯỚNG DẪN SỬ DỤNG:[/bold cyan]\n"
        "• Nhập cookie Facebook (ENTER để dừng nhập)\n"
        "• Nhập số lượng page muốn tạo\n"
        "• Thiết lập thời gian delay giữa các lần tạo",
        style="bright_blue",
        width=80
    )
    console.print(guide_panel)
    
    print()
    
    # Nhập cookie
    console.print("🔐 [bold yellow]NHẬP COOKIE FACEBOOK[/bold yellow]")
    console.print("[bold red](Nhấn ENTER để dừng nhập)[/bold red]")
    
    while True:
        tqntool.stt += 1
        cookie_fb = input(f'\033[1;35m🍪 Cookie thứ [{tqntool.stt}]:\033[1;34m ')
        if cookie_fb == '':
            break
        
        if not tqntool.validate_cookie(cookie_fb):
            tqntool.stt -= 1
            console.print("❌ [red]Cookie không hợp lệ![/red]")
            continue
        
        checklive = tqntool.getthongtinfacebook(cookie_fb)
        if checklive:
            console.print(f"✅ [green]Live[/green] | Name: [cyan]{checklive[0]}[/cyan] | UID: [yellow]{checklive[1]}[/yellow]")
            tqntool.list_clone.append(f'{cookie_fb}|{checklive[0]}|{checklive[1]}|{checklive[2]}|{checklive[3]}')
        else:
            tqntool.stt -= 1
            console.print(f"❌ [red]Die[/red] | Cookie không hợp lệ hoặc mất kết nối!")
    
    if not tqntool.list_clone:
        console.print("[bold red]⚠️ Không có cookie hợp lệ nào được nhập![/bold red]")
        return
    
    console.print(f"[bold green]🎯 Đã nhập: {len(tqntool.list_clone)} cookie hợp lệ[/bold green]")
    
    # Nhập setting
    console.print("\n⚙️ [bold yellow]THIẾT LẬP CÀI ĐẶT[/bold yellow]")
    
    try:
        tqntool.slpage = int(input('🎯 Số lượng page muốn tạo: '))
    except:
        tqntool.slpage = 10
        console.print(f"[yellow]Sử dụng mặc định: {tqntool.slpage} page[/yellow]")
    
    try:
        delay = int(input('⏰ Thời gian delay (giây): '))
        if delay < 5:
            delay = 5
            console.print("[yellow]Delay tối thiểu là 5 giây để tránh bị chặn[/yellow]")
    except:
        delay = 10
        console.print(f"[yellow]Sử dụng mặc định: {delay} giây[/yellow]")
    
    # Hiển thị thống kê
    tqntool.banner()
    tqntool.show_stats()
    
    # Panel bắt đầu
    start_panel = Panel(
        "🚀 [bold green]BẮT ĐẦU QUÁ TRÌNH TẠO PAGE...[/bold green]",
        style="bold green",
        width=80
    )
    console.print(start_panel)
    
    # Chạy tool với Progress Bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("•"),
        TextColumn("[bold green]{task.completed}[/bold green]/[bold cyan]{task.total}[/bold cyan]"),
    ) as progress:
        
        main_task = progress.add_task("[cyan]Đang tạo page...", total=tqntool.slpage)
        retry_count = 0
        max_retries = 3
        
        while tqntool.dem < tqntool.slpage:
            for dulieuclone in tqntool.list_clone:
                if tqntool.dem >= tqntool.slpage:
                    break
                    
                data_parts = str(dulieuclone).split('|')
                if len(data_parts) >= 5:
                    success, page_id, page_name = tqntool.RegPage(
                        data_parts[0], data_parts[1], data_parts[2], 
                        data_parts[3], data_parts[4]
                    )
                    
                    if success:
                        retry_count = 0
                        console.print(f"   💾 [blue]Đã lưu page: {page_name} (ID: {page_id})[/blue]")
                    else:
                        retry_count += 1
                        if retry_count >= max_retries:
                            console.print(f"⚠️ [yellow]Đã thử {max_retries} lần thất bại, chuyển cookie khác[/yellow]")
                            retry_count = 0
                            continue
                    
                    progress.update(main_task, completed=tqntool.dem)
                    tqntool.tqn_delay_tool(delay)
            
            if tqntool.dem >= tqntool.slpage:
                break
            
            # Nếu đã duyệt hết cookie mà chưa đạt đủ số lượng
            console.print("🔄 [yellow]Đã duyệt hết cookie, bắt đầu lại...[/yellow]")
    
    # Kết thúc
    console.print(f"\n🎉 [bold green]HOÀN THÀNH! ĐÃ TẠO {tqntool.dem} PAGE[/bold green]")
    
    # Hiển thị thông tin file JSON
    filename = f"created_pages_{datetime.now().strftime('%d%m%Y')}.json"
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        console.print(f"📁 [bold cyan]File: {filename}[/bold cyan] | 📊 [bold yellow]Tổng số page: {len(data)}[/bold yellow]")
    
    # Panel kết thúc
    end_panel = Panel(
        f"✅ [bold green]CÔNG VIỆC HOÀN TẤT![/bold green]\n"
        f"📊 Tổng số page đã tạo: [bold yellow]{tqntool.dem}[/bold yellow]\n"
        f"💾 Dữ liệu đã được lưu tự động vào file JSON\n"
        f"🔒 Đã bảo vệ với delay tối thiểu 5 giây để tránh bị chặn",
        style="bold green",
        width=80
    )
    console.print(end_panel)
    
    input('\n🎯 Nhấn ENTER để thoát...')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console = Console()
        console.print("\n⚠️ [yellow]Đã dừng tool bởi người dùng[/yellow]")
    except Exception as e:
        console = Console()
        console.print(f"\n❌ [red]Lỗi không mong đợi: {e}[/red]")
        input("\nNhấn ENTER để thoát...")