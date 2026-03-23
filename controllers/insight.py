import datetime
import io
import json
import os


import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from matplotlib import pyplot as plt


class InsightController:
   def __init__(self, main_view):
       self.view = main_view


############################ XỬ LÍ LOGIC ############################################
   def kiemTraTrangHienTai(self, index):
       if self.view.stackedWidget.widget(index) == self.view.pageInsight:
           try:
               self.updateTienDoHocTap()
               self.updateInsight()
           except Exception as e:
               print(f"LỖI KHI CHUYỂN TAB INSIGHT: {e}")
               import traceback
               traceback.print_exc()


   def updateTienDoHocTap(self):
       danh_sach_mon = self.view.sub_manager.list
       tong_tin_chi_da_hoc = 0
       for mon_hoc in danh_sach_mon:
           tong_tin_chi_da_hoc += float(mon_hoc.credit)


       Tong_tin_chi = 130
       phan_tram = 0
       if Tong_tin_chi > 0:
           phan_tram = (tong_tin_chi_da_hoc / Tong_tin_chi) * 100
       self.view.lineEditInputTienDo.setText(f"{phan_tram:.2f}%")


   def layTongChiTieuThang(self, thang, nam):
       tong = 0
       items = self.view.expense_manager.items
       for item in items:
           date_obj = datetime.datetime.strptime(item.ngay, "%d/%m/%Y")
           if date_obj.month == thang and date_obj.year == nam:
               tong += item.so_tien
       return tong


   def layGPAKyTruoc(self):
       path = f"../datasets/{self.current_acc}_gpa_user.json"
       # Nếu file KHÔNG TỒN TẠI -> Tự động tạo luôn file mới với điểm 0.0
       if not os.path.exists(path):
           du_lieu_mac_dinh = {"gpa_ky_truoc": 0.0}
           with open(path, "w", encoding="utf-8") as f:
               json.dump(du_lieu_mac_dinh, f, indent=4)
           return 0.0  # Trả về 0.0 cho lần chạy đầu tiên


       with open(path, "r", encoding="utf-8") as f:
           data = json.load(f)
           return float(data.get("gpa_ky_truoc", 0.0))


####################### VẼ BIỂU ĐỒ #######################
   def veBieuDoTrend(self, gpa_cu, gpa_hien_tai):
       fig, ax = plt.subplots(figsize=(4, 1.5), dpi=100)
       fig.patch.set_alpha(0)
       ax.set_facecolor('none')
       x = ["Trước", "Hiện tại"]
       y = [gpa_cu, gpa_hien_tai]
       color = '#27ae60' if gpa_hien_tai >= gpa_cu else '#c0392b'
       ax.plot(x, y, marker='o', color=color, linewidth=2.5, markersize=8)


       khoang_cach = 0.5
       ax.set_ylim(min(y) - khoang_cach, max(y) + khoang_cach)
       ax.spines['top'].set_visible(False)
       ax.spines['right'].set_visible(False)
       ax.spines['bottom'].set_visible(False)
       ax.spines['left'].set_visible(False)
       ax.get_yaxis().set_visible(False)


       for i, v in enumerate(y):
           ax.text(i, v + 0.15, f"{v:.2f}", ha='center', color=color, fontweight='bold')
       plt.tight_layout()
       buf = io.BytesIO()


       plt.savefig(buf, format='png', transparent=True, bbox_inches='tight')
       plt.close(fig)
       buf.seek(0)
       qimg = QImage.fromData(buf.getvalue())
       return QPixmap.fromImage(qimg)


   def updateInsight(self):
       try:
############################## TÍNH GPA ###################################
           tong_tin_chi_tich_luy = 0
           tong_diem_tich_luy = 0.0
           danh_sach = self.view.sub_manager.list
           for mon in danh_sach:
               tin_chi = float(mon.credit)
               diem_so =(float(mon.scoreProcess) * 0.2) + (float(mon.scoreMidterm) * 0.3) + (float(mon.scoreFinal) * 0.5)
               tong_tin_chi_tich_luy += tin_chi
               tong_diem_tich_luy += (diem_so * tin_chi)
           GPA = 0.0
           if tong_tin_chi_tich_luy > 0:
               GPA = tong_diem_tich_luy / tong_tin_chi_tich_luy
           self.view.lineEditInputGPA.setText(f"{GPA:.2f}")
           self.view.lineEditInputGPA.setReadOnly(True)
           self.view.insight_GPA.setText(f"{GPA:.2f}")


           TONG_TIN_CHI_RA_TRUONG = 130
           phan_tram_tiendo = 0.0
           if tong_tin_chi_tich_luy > 0:
               phan_tram_tiendo = (tong_tin_chi_tich_luy / TONG_TIN_CHI_RA_TRUONG) * 100
           if phan_tram_tiendo > 100: phan_tram_tiendo = 100
           text_tiendo = f"{phan_tram_tiendo:.2f}%"
           self.view.lineEditInputTienDo.setText(text_tiendo)
           self.view.lineEditInputTienDo.setReadOnly(True)


           # So sánh GPA cũ
           gpa_cu = self.layGPAKyTruoc()
           chenh_lech = GPA - gpa_cu
           if chenh_lech >= 0:
               text = f"↑ Tăng {chenh_lech:.2f} so với lần cập nhật trước"
               color = "green"
           else:
               text = f"↓ Giảm {abs(chenh_lech):.2f} so với lần cập nhật trước"
               color = "red"
           self.view.number1_2.setText(text)
           self.view.number1_2.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 12px;")


           pixmap_chart = self.veBieuDoTrend(gpa_cu, GPA)
           self.view.label_linechart.setPixmap(pixmap_chart)
           self.view.label_linechart.setScaledContents(True)
           self.view.label_linechart.setAlignment(Qt.AlignmentFlag.AlignCenter)


####################### XỬ LÝ TÀI CHÍNH ###############################
           so_du = self.view.balance_manager.current_balance
           self.view.lineEditInputTienDo_2.setText(f"{so_du:,.0f} VNĐ")
           self.view.lineEditInputTienDo_2.setReadOnly(True)
######################## TOP SPENDING #######################
           danh_sach_chi_tieu = {}
           tong_tien_chi_tieu = 0.0
           items_chi_tieu = self.view.expense_manager.items
           for item in items_chi_tieu:
               muc_dich = item.danh_muc.lower() if item.danh_muc else "khác"
                   # Xử lý số tiền
               tien_str = str(item.so_tien).replace(',', '').replace('.', '')
               tien = float(item.so_tien)
               if not str(tien).replace('.', '', 1).isdigit() and tien_str.isdigit():
                   tien = float(tien_str)
               if muc_dich in danh_sach_chi_tieu:
                   danh_sach_chi_tieu[muc_dich] += tien
               else:
                   danh_sach_chi_tieu[muc_dich] = tien
               tong_tien_chi_tieu += tien
######################## HIỂN THỊ ICON TOP SPENDING #######################
           if danh_sach_chi_tieu:
               top_cat = max(danh_sach_chi_tieu, key=danh_sach_chi_tieu.get)
               top_val = danh_sach_chi_tieu[top_cat]
                   # Tính phần trăm
               percent = (top_val / tong_tien_chi_tieu) * 100 if tong_tien_chi_tieu > 0 else 0
               self.view.number2_2.setText(f"{percent:.1f}%")
               top_cat = top_cat.lower()
               icon_map = {
                       "mua sắm": "../images/mua_sam.png",
                       "ăn uống": "../images/food.png",
                       "học tập": "../images/study.png",
                       "đi lại": "../images/xe_co.png",
                       "giải trí": "../images/tro_choi.png",
                       "sức khỏe": "../images/y_te.png"
                   }
               icon = icon_map.get(top_cat)
               if icon:
                   self.view.topspending.setPixmap(QPixmap(icon))
                   self.view.topspending.setScaledContents(True)
####################### PHẦN TIPS & LỜI KHUYÊN #######################
           chitieu_thang_nay = tong_tien_chi_tieu
           so_du = self.view.balance_manager.current_balance


           # --- 1. XỬ LÝ TÀI CHÍNH ---
           if so_du <= 0:
               if chitieu_thang_nay > 0:
                   ap_luc_tai_chinh = float('inf')
                   muc_chi_tieu = "BAO_DONG"
               else:
                   ap_luc_tai_chinh = 0.0
                   muc_chi_tieu = "THIEU_DU_LIEU_TC"
           else:
               ap_luc_tai_chinh = chitieu_thang_nay / so_du
               if ap_luc_tai_chinh > 1.5:
                   muc_chi_tieu = "BAO_DONG"
               elif ap_luc_tai_chinh > 0.7:
                   muc_chi_tieu = "CANH_BAO"
               else:
                   muc_chi_tieu = "AN_TOAN"


           # --- 2. XỬ LÝ HỌC THUẬT & XU HƯỚNG ---
           if GPA >= 8.0:
               muc_gpa = "XUAT_SAC"
           elif GPA >= 6.5:
               muc_gpa = "KHA"
           elif GPA >= 5.0:
               muc_gpa = "TRUNG_BINH"
           else:
               muc_gpa = "NGUY_HIEM"


           gpa_cu = self.layGPAKyTruoc()
           gpa_trend = GPA - gpa_cu if gpa_cu > 0 else 0
           trend_msg = ""
           gpa_penalty = 0
           is_rewarded = False




           if gpa_cu > 0:
               if gpa_trend <= -1.0:
                   gpa_penalty = 1  # Chỉ phạt 1 bậc thay vì 2
                   trend_msg = "⚠️ PHONG ĐỘ SỤT GIẢM: Bạn đang mất đà học tập nghiêm trọng so với kỳ trước!"
               elif gpa_trend <= -0.5:
                   gpa_penalty = 0  # Không phạt bậc, nhưng cảnh báo bằng lời
                   trend_msg = "📉 LƯU Ý: Điểm số có dấu hiệu đi xuống, hãy cẩn thận!"
               elif gpa_trend >= 0.5:
                   is_rewarded = True
                   trend_msg = "📈 TÍCH CỰC: Điểm số đang bứt phá rất ấn tượng!"


           # Dùng Tuple (Immutable) thay vì List để tối ưu bộ nhớ & an toàn dữ liệu
           LEVELS = ("NGUY_HIEM", "TRUNG_BINH", "KHA", "XUAT_SAC")
           current_idx = LEVELS.index(muc_gpa)
           effective_idx = max(0, current_idx - gpa_penalty)
           muc_gpa_effective = LEVELS[effective_idx]


           # --- 3. MA TRẬN QUYẾT ĐỊNH (Exhaustive Semantic Handling) ---
           nhanxet, tips, ghichu = "", "", ""
           color_bg, color_text = "#FFFFFF", "black"


           # Case 0: Trống trơn dữ liệu
           if tong_tin_chi_tich_luy == 0 and muc_chi_tieu == "THIEU_DU_LIEU_TC":
               nhanxet = "Chào mừng! Hệ thống đang chờ dữ liệu từ bạn."
               tips = "Hãy cập nhật điểm số và chi phí để kích hoạt AI Phân tích."
               ghichu = "CHƯA CÓ DATA"
               color_bg = "#E0E0E0"


           # Case 1: Nguy hiểm
           elif muc_gpa_effective == "NGUY_HIEM":
               color_bg, color_text = "#FF6961", "white"
               ghichu = "CỨU GẤP (RỚT MÔN)"
               if muc_chi_tieu == "BAO_DONG":
                   nhanxet = "THẢM HỌA KÉP: Rớt môn và Cạn kiệt tài chính!"
                   tips = "Tình trạng báo động tối đa. Ngưng chi giải trí, ưu tiên đóng tiền học lại!"
               elif muc_chi_tieu == "THIEU_DU_LIEU_TC":
                   nhanxet = "Nguy cơ rớt môn cực cao! (Chưa rõ tài chính)"
                   tips = "Hãy cập nhật ví tiền. Khóa cửa phòng và ôn lại toàn bộ kiến thức gốc ngay!"
               elif muc_chi_tieu == "CANH_BAO":
                   nhanxet = "GPA báo động đỏ, tài chính cũng hao hụt nhanh!"
                   tips = "Dành toàn bộ thời gian và ngân sách còn lại cho việc học lại/thi lại."
               else:  # AN_TOAN
                   nhanxet = "Nguy cơ rớt môn cực cao! (Tài chính tạm ổn)"
                   tips = "Bạn còn tiền, hãy đăng ký lớp tăng cường. Bắt tay vào học ngay!"


           # Case 2: Trung Bình
           elif muc_gpa_effective == "TRUNG_BINH":
               color_bg = "#FFCAA1"
               ghichu = "CẦN CỐ GẮNG"
               if muc_chi_tieu == "BAO_DONG":
                   nhanxet = "Điểm lẹt đẹt, ví tiền lại chạm đáy!"
                   tips = "Cắt giảm ăn ngoài và nghiêm túc lập thời gian biểu học tập mỗi tối."
               elif muc_chi_tieu == "THIEU_DU_LIEU_TC":
                   nhanxet = "Học lực trung bình (Hệ thống chưa rõ tài chính)."
                   tips = "Cập nhật dòng tiền ngay. Đồng thời, thiết lập kỷ luật học tập để cải thiện điểm số."
               elif muc_chi_tieu == "CANH_BAO":
                   nhanxet = "Học lực trung bình, chi tiêu bắt đầu rủi ro."
                   tips = "Cẩn thận! Hạn chế tiêu xài để phòng hờ chi phí thi lại/học lại."
               else:  # AN_TOAN
                   nhanxet = "Tài chính an toàn, nhưng điểm số cần bứt phá."
                   tips = "Dùng số dư tài chính mua thêm tài liệu để tối ưu hiệu suất học nhé."


           # Case 3: Khá
           elif muc_gpa_effective == "KHA":
               is_low_kha = (GPA < 7.0)
               if muc_chi_tieu == "BAO_DONG":
                   color_bg = "#FDFD96"
                   nhanxet = "Điểm Khá, nhưng tài chính đang mất kiểm soát!"
                   tips = "Dừng ngay việc mua sắm bốc đồng. Học phí kỳ tới có thể là gánh nặng đấy."
                   ghichu = "SIẾT CHI TIÊU"
               elif muc_chi_tieu == "THIEU_DU_LIEU_TC":
                   color_bg = "#A1E8AF"
                   nhanxet = "Điểm Khá ổn (Hệ thống chưa rõ tài chính)."
                   tips = "Nhớ cập nhật chi tiêu nhé. Về học tập, thử học nhóm để củng cố kiến thức vững hơn."
                   ghichu = "CHỜ DATA TÀI CHÍNH"
               elif muc_chi_tieu == "CANH_BAO":
                   color_bg = "#FDFD96"
                   nhanxet = "Học khá ổn, nhưng ví tiền hao hụt hơi nhanh."
                   tips = "Áp dụng quy tắc 24h trước khi quyết định mua món đồ tiếp theo."
                   ghichu = "CHÚ Ý TÀI CHÍNH"
               else:  # AN_TOAN
                   color_bg = "#A1E8AF"
                   ghichu = "ỔN ĐỊNH"
                   if is_low_kha:
                       nhanxet = "Đạt mức Khá, nhưng điểm số chưa thực sự vững vàng."
                       tips = "Chỉ cần xao nhãng là rớt xuống Trung Bình. Thử nhóm học tập để củng cố kiến thức."
                   else:
                       nhanxet = "Bạn đang duy trì mức Khá rất an toàn."
                       tips = "Thử thách bản thân với một bài tập khó hơn để lấy đà lên 8.0+ xem sao!"


           # Case 4: Xuất Sắc
           else:
               if muc_chi_tieu == "BAO_DONG":
                   color_bg = "#FDFD96"
                   nhanxet = "Học cực giỏi! Nhưng đang vung tay quá trán."
                   tips = "Đừng biến thành tích thành lý do để tiêu sạch tiền. Trích 20% cất đi ngay."
                   ghichu = "CẢNH BÁO VÍ TIỀN"
               elif muc_chi_tieu == "THIEU_DU_LIEU_TC":
                   color_bg = "#63A693";
                   color_text = "white"
                   nhanxet = "Học cực giỏi! (Hệ thống chưa rõ tài chính)."
                   tips = "Đừng quên ghi chép chi tiêu để quản lý tài chính xuất sắc như cách bạn học nhé!"
                   ghichu = "XUẤT SẮC"
               elif muc_chi_tieu == "CANH_BAO":
                   color_bg = "#A1E8AF"
                   nhanxet = "Thành tích tuyệt vời, tài chính ở mức vừa vặn."
                   tips = "Không có gì để chê, nhưng nếu tiết kiệm được thêm một chút thì sẽ hoàn hảo hơn."
                   ghichu = "KHÁ TỐT"
               else:  # AN_TOAN
                   color_bg = "#63A693";
                   color_text = "white"
                   nhanxet = "Hoàn hảo! Học thủ khoa - Quản lý tiền như chuyên gia!"
                   tips = "Top 1% server! Hãy duy trì lối sống kỷ luật này và lan tỏa cho bạn bè nhé."
                   ghichu = "RẤT AN TOÀN"


           # --- 4. Gắn thêm Reward & Xử lý UX UI ---
           if is_rewarded:
               if muc_gpa_effective != "XUAT_SAC":
                   ghichu += " | ĐANG BỨT PHÁ 🚀"
               # Thêm lời động viên cực mạnh nếu có trend tốt
               tips += "\n🔥 Phong độ đang lên! Giữ vững đà này, bạn sẽ sớm chinh phục mốc điểm cao hơn!"


           # Đóng gói Trend Message bằng vách ngăn (Divider) để text không bị dính chùm
           if trend_msg:
               tips += f"\n -- \n{trend_msg}"


           # --- 5. RENDER UI ---
           self.view.advice_2.setText(nhanxet)
           self.view.advice_2.setStyleSheet(f"background-color:{color_bg}; color:{color_text}; font-weight:bold;")
           self.view.input_tips.setText(tips)
           self.view.shortcomment_2.setText(f"NOTE: {ghichu}")
           self.view.shortcomment_2.setStyleSheet(f"background-color:{color_bg}; color:{color_text}; font-weight:bold;")


       # QUAN TRỌNG: Đây là đoạn Catch Error lúc nãy bị bạn xóa mất do copy đè
       except Exception as e:
           print(f"LỖI NGHIÊM TRỌNG TRONG UPDATE INSIGHT: {e}")
           import traceback
           traceback.print_exc()


####################### XỬ LÍ XUẤT FILE EXCEL/CSV ##############################
   def process_excel_csv(self):
       msgBox = QMessageBox(self.view.MainWindow)
       msgBox.setIcon(QMessageBox.Icon.Question)
       msgBox.setWindowTitle("Tùy chọn xuất báo cáo")
       msgBox.setText("Bạn muốn tải báo cáo này về máy dưới định dạng nào?")
       btn_excel = msgBox.addButton("Excel (.xlsx)", QMessageBox.ButtonRole.ActionRole)
       btn_csv = msgBox.addButton("CSV (.csv)", QMessageBox.ButtonRole.ActionRole)
       btn_cancel = msgBox.addButton("Để sau", QMessageBox.ButtonRole.RejectRole)
       msgBox.exec()
       clicked_button = msgBox.clickedButton()
       if clicked_button == btn_excel:
           self.export_to_excel()
       elif clicked_button == btn_csv:
           self.export_to_csv()


   def lay_du_lieu_oversight(self):
       # Giao diện Qt đã nạp xong thì cứ thế mà gọi thẳng ra thôi, không cần check gì cả!
       val_gpa = self.view.lineEditInputGPA.text()
       val_tiendo = self.view.lineEditInputTienDo.text()
       val_vitien = self.view.lineEditInputTienDo_2.text()
       val_nhanxet = self.view.advice_2.text()
       val_tips = self.view.input_tips.toPlainText()
       data = {
           "HẠNG MỤC": ["GPA Hiện tại", "Tiến độ học tập", "Số dư tài chính", "Đánh giá tổng quan",
                        "Lời khuyên chi tiết"],"KẾT QUẢ": [val_gpa, val_tiendo, val_vitien, val_nhanxet, val_tips]}
       return pd.DataFrame(data)


   def export_to_excel(self):
       df = self.lay_du_lieu_oversight()
       thoi_gian = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
       ten_mac_dinh = f"BaoCao_TongQuan_{thoi_gian}.xlsx"
       duong_dan, _ = QFileDialog.getSaveFileName(
           self.view.MainWindow,"Lưu báo cáo Excel",ten_mac_dinh,"Excel Files (*.xlsx)")
       if duong_dan:
           df.to_excel(duong_dan, index=False, engine='openpyxl')
           QMessageBox.information(self.view.MainWindow, "Thành công!",f"Báo cáo của bạn đã được lưu an toàn tại:\n{duong_dan}")


   def export_to_csv(self):
       df = self.lay_du_lieu_oversight()
       thoi_gian = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
       ten_mac_dinh = f"BaoCao_TongQuan_{thoi_gian}.csv"
       duong_dan, _ = QFileDialog.getSaveFileName(self.view.MainWindow,"Lưu báo cáo CSV",ten_mac_dinh,"CSV Files (*.csv)")
       if duong_dan:
           df.to_csv(duong_dan, index=False, encoding='utf-8-sig')
           QMessageBox.information(self.view.MainWindow, "Thành công!",f"Báo cáo của bạn đã được lưu an toàn tại:\n{duong_dan}")