import datetime
import io
import json
import os
import random

import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from matplotlib import pyplot as plt


class InsightController:
    def __init__(self, main_view):
        self.view = main_view

############################ XỬ LÍ LOGIC ############################################
    def kiem_tra_trang_hien_tai(self, index):
        if self.view.stackedWidget.widget(index) == self.view.pageInsight:
            try:
                self.update_tiendo_hoctap()
                self.updateinsight()
            except Exception as e:
                print(f"LỖI KHI CHUYỂN TAB INSIGHT: {e}")
                import traceback
                traceback.print_exc()

    def update_tiendo_hoctap(self):
        danh_sach_mon = self.view.sub_manager.list
        tong_tin_chi_da_hoc = 0
        for mon_hoc in danh_sach_mon:
            tong_tin_chi_da_hoc += float(mon_hoc.credit)

        Tong_tin_chi = 130
        phan_tram = 0
        if Tong_tin_chi > 0:
            phan_tram = (tong_tin_chi_da_hoc / Tong_tin_chi) * 100
        self.view.lineEditInputTienDo.setText(f"{phan_tram:.2f}%")

    def lay_tong_chi_tieu_thang(self, thang, nam):
        tong = 0
        items = self.view.expense_manager.items
        for item in items:
            date_obj = datetime.datetime.strptime(item.ngay, "%d/%m/%Y")
            if date_obj.month == thang and date_obj.year == nam:
                tong += item.so_tien
        return tong

    def lay_gpa_ky_truoc(self):
        path = f"../datasets/{self.current_acc}_gpa_user.json"
        if not os.path.exists(path): return 0.0
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return float(data.get("gpa_ky_truoc", 0.0))

####################### VẼ BIỂU ĐỒ #######################
    def ve_bieu_do_trend(self, gpa_cu, gpa_hien_tai):
        fig, ax = plt.subplots(figsize=(4, 1.5), dpi=100)
        fig.patch.set_alpha(0)
        ax.set_facecolor('none')
        x = ["Kỳ trước", "Kỳ này"]
        y = [gpa_cu, gpa_hien_tai]
        color = '#27ae60' if gpa_hien_tai >= gpa_cu else '#c0392b'
        ax.plot(x, y, marker='o', color=color, linewidth=2.5, markersize=8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_yaxis().set_visible(False)
        for i, v in enumerate(y):
            ax.text(i, v + 0.1, f"{v:.2f}", ha='center', color=color, fontweight='bold')
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', transparent=True)
        plt.close(fig)
        buf.seek(0)
        qimg = QImage.fromData(buf.getvalue())
        return QPixmap.fromImage(qimg)

    def updateinsight(self):
        try:
############################## TÍNH GPA ###################################
            tong_tin_chi_tich_luy = 0
            tong_diem_tich_luy = 0.0
            danh_sach = self.view.sub_manager.list
            for mon in danh_sach:
                tin_chi = float(mon.credit)
                diem_so = float(mon.scoreFinal)
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
            gpa_cu = self.lay_gpa_ky_truoc()
            chenh_lech = GPA - gpa_cu
            if chenh_lech >= 0:
                text = f"↑ Tăng {chenh_lech:.2f} so với kỳ trước"
                color = "green"
            else:
                text = f"↓ Giảm {abs(chenh_lech):.2f} so với kỳ trước"
                color = "red"
            self.view.number1_2.setText(text)
            self.view.number1_2.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 12px;")

            pixmap_chart = self.ve_bieu_do_trend(gpa_cu, GPA)
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
            #Tiêu quá 3 triệu rưỡi/tháng là cảnh báo
            bi_lo_tay = False
            if chitieu_thang_nay > 3500000:
                bi_lo_tay = True
            tip_tietkiem = ["Tách riêng 2 ví: 1 tiêu dùng - 1 tiết kiệm. Đừng để chung!","Chia nhỏ ngân sách: Đặt hạn mức theo tuần thay vì tháng.","Quy tắc 24h: Tự hỏi bản thân cần hay muốn? Và chờ 1-2 ngày trước khi mua."," Ưu tiên cơm nhà: Vừa an toàn, sạch sẽ lại vừa tiết kiệm.","Ghi chép chi vặt: Trà sữa, ship đồ ăn chính là thủ phạm gây cháy túi!","Đừng quên quyền năng thẻ sinh viên: Giảm giá khắp mọi nơi!","Quẹt thẻ thì sướng, trả tiền mặt mới thấy xót. Hãy dùng tiền mặt!"]

            tip_caithien = ["Hổng kiến thức khiến GPA thấp. Hãy ôn lại cơ bản ngay!","Thử Pomodoro: 25 phút Học - 5 phút nghỉ.","Đừng ngại hỏi giảng viên hoặc bạn bè khi chưa hiểu bài.","Tập trung tuyệt đối: Tắt thông báo điện thoại khi đang học.","Ghi chép thông minh: Sử dụng sơ đồ tư duy (mindmap) để hệ thống bài học.","Đừng học vẹt! Hãy hiểu rõ bản chất vấn đề!!","Review lại bài ngay sau khi học xong giúp nhớ lâu gấp 3 lần!!","Phương pháp Feynman: Thử giảng lại kiến thức cho người khác để hiểu sâu hơn!"]

            tip_hoctot = ["Phong độ rất tốt! Hãy duy trì thói quen hiện tại.","Đừng quên cân bằng giữa học và chơi để tránh Burn-out.","Bạn có thể bắt đầu tìm kiếm học bổng hoặc tham gia nghiên cứu.","Hãy thử thách bản thân với các môn học khó hơn.","Chia sẻ kiến thức với bạn bè cũng là cách để ôn bài hiệu quả.","Chuẩn bị sớm cho các chứng chỉ ngoại ngữ hoặc kỹ năng mềm.","Giữ sức khỏe! Ngủ đủ giấc giúp não bộ hoạt động tối ưu."]

            nhanxet = ""
            tips = ""
            ghichu = ""
            # Logic chọn lời khuyên
            if GPA >= 8.0 and bi_lo_tay is False:
                nhanxet = "Xuất sắc! Học giỏi - Tài chính vững!"
                self.view.advice_2.setStyleSheet("background-color:#63A693; color:black; font-weight:bold;")
                tips = random.choice(tip_hoctot)
                ghichu = "NOTE: AN TOÀN"
                self.view.shortcomment_2.setStyleSheet("background-color:#63A693; color:white; font-weight:bold;")
            elif GPA >= 8.0 and bi_lo_tay is True:
                nhanxet = "Học tốt! Nhưng xài tiền hơi lố."
                self.view.advice_2.setStyleSheet("background-color:#FDFD96; color:black; font-weight:bold;")
                tips = random.choice(tip_tietkiem)
                ghichu = "NOTE: CẢNH BÁO"
                self.view.shortcomment_2.setStyleSheet("background-color:#FFCAA1; color:black; font-weight:bold;")
            elif GPA < 8.0 and bi_lo_tay is False:
                if GPA >= 6.5:
                    nhanxet = "Học lực Khá! Tài chính ổn."
                else:
                    nhanxet = "Cảnh báo học tập!"
                self.view.advice_2.setStyleSheet("background-color:#FDFD96; color:black; font-weight:bold;")
                tips = random.choice(tip_caithien)
                ghichu = "NOTE: CẢNH BÁO"
                self.view.shortcomment_2.setStyleSheet("background-color:#FFCAA1; color:black; font-weight:bold;")
            elif GPA < 8.0 and bi_lo_tay is True:
                nhanxet = "BÁO ĐỘNG ĐỎ: Tiền và Điểm đều nguy cấp!"
                self.view.advice_2.setStyleSheet("background-color:#FF6961; color:white; font-weight:bold;")
                tips = random.choice(tip_tietkiem)
                ghichu = "NOTE: BÁO ĐỘNG ĐỎ"
                self.view.shortcomment_2.setStyleSheet("background-color:#FF6961; color:white; font-weight:bold;")
            self.view.advice_2.setText(nhanxet)
            self.view.input_tips.setText(tips)
            self.view.shortcomment_2.setText(ghichu)
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