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

    ############################ XỬ LÍ LOGIC GPA ############################################
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
        try:
            if not hasattr(self.view, 'sub_manager'): return

            danh_sach_mon = self.view.sub_manager.list
            tong_tin_chi_da_hoc = 0
            for mon_hoc in danh_sach_mon:
                try:
                    tong_tin_chi_da_hoc += float(mon_hoc.credit)
                except:
                    continue
            Tong_tin_chi = 130
            phan_tram = 0
            if Tong_tin_chi > 0:
                phan_tram = (tong_tin_chi_da_hoc / Tong_tin_chi) * 100

            # Kiểm tra tồn tại widget trước khi gán
            if hasattr(self.view, 'lineEdit_TienDo'):
                self.view.lineEdit_TienDo.setText(f"{phan_tram:.2f}%")
        except Exception as e:
            print(f"Lỗi update_tiendo_hoctap: {e}")

    def lay_tong_chi_tieu_thang(self, thang, nam):
        tong = 0
        if not hasattr(self.view, 'expense_manager'):
            return 0

        for item in self.view.expense_manager.items:
            try:
                date_obj = datetime.datetime.strptime(item.ngay, "%d/%m/%Y")
                if date_obj.month == thang and date_obj.year == nam:
                    tong += item.so_tien
            except:
                continue
        return tong

    def lay_gpa_ky_truoc(self):
        try:
            path = "../datasets/gpa_user.json"
            if not os.path.exists(path): return 0.0

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return float(data.get("gpa_ky_truoc", 0.0))
        except:
            return 0.0

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
            # =========================================================================
            # PHẦN 1: TÍNH TOÁN GPA & TIẾN ĐỘ
            # =========================================================================
            tong_tin_chi_tich_luy = 0
            tong_diem_tich_luy = 0.0

            # 1.1 Quét danh sách môn học
            if hasattr(self.view, 'sub_manager') and hasattr(self.view.sub_manager, 'list'):
                for mon in self.view.sub_manager.list:
                    try:
                        tin_chi = float(mon.credit)
                        diem_so = float(mon.scoreFinal)

                        tong_tin_chi_tich_luy += tin_chi
                        tong_diem_tich_luy += (diem_so * tin_chi)
                    except (ValueError, AttributeError):
                        continue

            GPA = 0.0
            if tong_tin_chi_tich_luy > 0:
                GPA = tong_diem_tich_luy / tong_tin_chi_tich_luy

            # Hiển thị GPA
            if hasattr(self.view, 'lineEditInputGPA'):
                self.view.lineEditInputGPA.setText(f"{GPA:.2f}")
                self.view.lineEditInputGPA.setReadOnly(True)
            if hasattr(self.view, 'insight_GPA'):
                self.view.insight_GPA.setText(f"{GPA:.2f}")

            # 1.3 Tính & Hiển thị Tiến Độ
            TONG_TIN_CHI_RA_TRUONG = 130
            phan_tram_tiendo = 0.0

            if tong_tin_chi_tich_luy > 0:
                phan_tram_tiendo = (tong_tin_chi_tich_luy / TONG_TIN_CHI_RA_TRUONG) * 100

            if phan_tram_tiendo > 100: phan_tram_tiendo = 100

            text_tiendo = f"{phan_tram_tiendo:.2f}%"

            if hasattr(self.view, 'lineEditInputTienDo'):
                self.view.lineEditInputTienDo.setText(text_tiendo)
                self.view.lineEditInputTienDo.setReadOnly(True)

            # 1.4 So sánh GPA cũ
            gpa_cu = self.lay_gpa_ky_truoc()
            chenh_lech = GPA - gpa_cu

            if hasattr(self.view, 'number1_2') and hasattr(self.view, 'insight_GPA'):
                if chenh_lech >= 0:
                    text = f"↑ Tăng {chenh_lech:.2f} so với kỳ trước"
                    color = "green"
                else:
                    text = f"↓ Giảm {abs(chenh_lech):.2f} so với kỳ trước"
                    color = "red"

                self.view.number1_2.setText(text)
                self.view.number1_2.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 12px;")
            if hasattr(self.view, 'label_linechart'):
                pixmap_chart = self.ve_bieu_do_trend(gpa_cu, GPA)
                self.view.label_linechart.setPixmap(pixmap_chart)
                self.view.label_linechart.setScaledContents(True)
                self.view.label_linechart.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # ========================================================================================
            # 2. XỬ LÝ TÀI CHÍNH
# ==========================================================================================
            so_du = 0.0
            if hasattr(self.view, 'balance_manager'):
                so_du = self.view.balance_manager.current_balance

            if hasattr(self.view, 'lineEditInputTienDo_2'):
                self.view.lineEditInputTienDo_2.setText(f"{so_du:,.0f} VNĐ")
                self.view.lineEditInputTienDo_2.setReadOnly(True)

# ==============================TOP SPENDING ====================================
            danh_sach_chi_tieu = {}
            tong_tien_chi_tieu = 0.0
            if hasattr(self.view, 'expense_manager') and hasattr(self.view.expense_manager, 'items'):
                for item in self.view.expense_manager.items:
                    try:
                        muc_dich = item.danh_muc.lower() if item.danh_muc else "khác"
                        # Xử lý số tiền
                        tien_str = str(item.so_tien).replace(',', '').replace('.', '')
                        try:
                            tien = float(item.so_tien)
                        except:
                            if tien_str.isdigit():
                                tien = float(tien_str)
                            else:
                                continue

                        if muc_dich in danh_sach_chi_tieu:
                            danh_sach_chi_tieu[muc_dich] += tien
                        else:
                            danh_sach_chi_tieu[muc_dich] = tien

                        tong_tien_chi_tieu += tien
                    except:
                        continue

# =======================HIỂN THỊ ICON TOP SPENDING ====================================
            if danh_sach_chi_tieu:
                top_cat = max(danh_sach_chi_tieu, key=danh_sach_chi_tieu.get)
                top_val = danh_sach_chi_tieu[top_cat]
                # Tính phần trăm
                percent = (top_val / tong_tien_chi_tieu) * 100 if tong_tien_chi_tieu > 0 else 0
                if hasattr(self.view, 'number2_2'):
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

                self.view.topspending.setPixmap(QPixmap(icon))
                self.view.topspending.setScaledContents(True)

#  ===================  PHẦN TIPS & LỜI KHUYÊN ============================================
            # Tính toán xem có bị lố tay không????
            today = datetime.datetime.now()
            chitieu_thang_nay = tong_tien_chi_tieu

            # Logic: Tiêu quá 2 trăm/tháng là cảnh báo
            bi_lo_tay = False
            if chitieu_thang_nay > 2000000:
                bi_lo_tay = True

            tip_tietkiem = ["Tách riêng 2 ví: 1 Tiêu dùng - 1 Tiết kiệm. Đừng để chung!",
                            "Chia nhỏ ngân sách: Đặt hạn mức theo Tuần thay vì Tháng.",
                            "Quy tắc 24h: Tự hỏi bản thân cần hay muốn? và chờ 1-2 ngày trước khi mua.",
                            " Ưu tiên cơm nhà: Vừa an toàn, sạch sẽ lại vừa tiết kiệm.",
                            "Ghi chép chi vặt: Trà sữa, ship đồ ăn chính là thủ phạm gây cháy túi!",
                            "Đừng quên quyền năng thẻ Sinh Viên: Giảm giá khắp mọi nơi!",
                            "Quẹt thẻ thì sướng, trả tiền mặt mới thấy xót. Hãy dùng tiền mặt!"]

            tip_caithien = [
                "Hổng kiến thức khiến GPA thấp. Hãy ôn lại cơ bản ngay!",
                "Thử Pomodoro: 25 phút Học - 5 phút Nghỉ.",
                "Đừng ngại hỏi giảng viên hoặc bạn bè khi chưa hiểu bài.",
                "Tập trung tuyệt đối: Tắt thông báo điện thoại khi đang học.",
                "Ghi chép thông minh: Sử dụng sơ đồ tư duy (Mindmap) để hệ thống bài học.",
                "Đừng học vẹt! Hãy hiểu rõ bản chất vấn đề!!",
                "Review lại bài ngay sau khi học xong giúp nhớ lâu gấp 3 lần!!",
                "Phương pháp Feynman: Thử giảng lại kiến thức cho người khác để hiểu sâu hơn!"
            ]
            tip_hoctot = ["Phong độ rất tốt! Hãy duy trì thói quen hiện tại.",
                          "Đừng quên cân bằng giữa học và chơi để tránh Burn-out.",
                          "Bạn có thể bắt đầu tìm kiếm học bổng hoặc tham gia nghiên cứu.",
                          "Hãy thử thách bản thân với các môn học khó hơn.",
                          "Chia sẻ kiến thức với bạn bè cũng là cách để ôn bài hiệu quả.",
                          "Chuẩn bị sớm cho các chứng chỉ ngoại ngữ hoặc kỹ năng mềm.",
                          "Giữ sức khỏe! Ngủ đủ giấc giúp não bộ hoạt động tối ưu."
                          ]

            nhanxet = ""
            tips = ""
            ghichu = ""

            # Logic chọn lời khuyên
            if GPA >= 8.0 and bi_lo_tay is False:
                nhanxet = "Xuất sắc! Học giỏi - Tài chính vững!"
                if hasattr(self.view, 'advice_2'):
                    self.view.advice_2.setStyleSheet(
                    "background-color:#63A693; color:black; font-weight:bold;")
                tips = random.choice(tip_hoctot)
                ghichu = "NOTE: AN TOÀN"
                if hasattr(self.view, 'shortcomment_2'):
                    self.view.shortcomment_2.setStyleSheet(
                    "background-color:#63A693; color:white; font-weight:bold;")

            elif GPA >= 8.0 and bi_lo_tay is True:
                nhanxet = "Học tốt! Nhưng xài tiền hơi lố."
                if hasattr(self.view, 'advice_2'):
                    self.view.advice_2.setStyleSheet(
                    "background-color:#FDFD96; color:black; font-weight:bold;")
                tips = random.choice(tip_tietkiem)
                ghichu = "NOTE: CẢNH BÁO"
                if hasattr(self.view, 'shortcomment_2'): self.view.shortcomment_2.setStyleSheet(
                    "background-color:#FFCAA1; color:black; font-weight:bold;")

            elif GPA < 8.0 and bi_lo_tay is False:
                if GPA >= 6.5:
                    nhanxet = "Học lực Khá! Tài chính ổn."
                else:
                    nhanxet = "Cảnh báo học tập!"
                if hasattr(self.view, 'advice_2'):
                    self.view.advice_2.setStyleSheet(
                    "background-color:#FDFD96; color:black; font-weight:bold;")
                tips = random.choice(tip_caithien)
                ghichu = "NOTE: CẢNH BÁO"
                if hasattr(self.view, 'shortcomment_2'):
                    self.view.shortcomment_2.setStyleSheet(
                    "background-color:#FFCAA1; color:black; font-weight:bold;")

            elif GPA < 8.0 and bi_lo_tay is True:
                nhanxet = "BÁO ĐỘNG ĐỎ: Tiền và Điểm đều nguy cấp!"
                if hasattr(self.view, 'advice_2'): self.view.advice_2.setStyleSheet(
                    "background-color:#FF6961; color:white; font-weight:bold;")
                tips = random.choice(tip_tietkiem)
                ghichu = "NOTE: BÁO ĐỘNG ĐỎ"
                if hasattr(self.view, 'shortcomment_2'): self.view.shortcomment_2.setStyleSheet(
                    "background-color:#FF6961; color:white; font-weight:bold;")

            # In kết quả
            if hasattr(self.view, 'advice_2'): self.view.advice_2.setText(nhanxet)
            if hasattr(self.view, 'input_tips'): self.view.input_tips.setText(tips)
            if hasattr(self.view, 'shortcomment_2'): self.view.shortcomment_2.setText(ghichu)

        except Exception as e:
            print(f"LỖI NGHIÊM TRỌNG TRONG UPDATE INSIGHT: {e}")
            import traceback
            traceback.print_exc()

        ####################### XỬ LÍ XUẤT FILE EXCEL/CSV##############################

    def process_excel_csv(self):
        try:
            msgBox = QMessageBox(self.view.MainWindow)
            msgBox.setIcon(QMessageBox.Icon.Question)
            msgBox.setWindowTitle("Xuất danh sách")
            msgBox.setText("Bạn muốn xuất file theo định dạng nào?")

            btn_excel = msgBox.addButton("EXCEL", QMessageBox.ButtonRole.ActionRole)
            btn_csv = msgBox.addButton("CSV", QMessageBox.ButtonRole.ActionRole)
            btn_cancel = msgBox.addButton("Hủy", QMessageBox.ButtonRole.RejectRole)

            msgBox.exec()

            clicked_button = msgBox.clickedButton()

            # Kiểm tra click
            if clicked_button == btn_excel:
                self.export_to_excel()
            elif clicked_button == btn_csv:
                self.export_to_csv()

        except Exception as e:
            print(f"Lỗi tại process_excel_csv: {e}")

    def lay_du_lieu_oversight(self):
        try:
            val_gpa = self.view.lineEditInputGPA.text() if hasattr(self.view, 'lineEditInputGPA') else ""
            val_tiendo = self.view.lineEditInputTienDo.text() if hasattr(self.view, 'lineEditInputTienDo') else ""
            val_vitien = self.view.lineEditInputTienDo_2.text() if hasattr(self.view, 'lineEditInputTienDo_2') else ""
            val_nhanxet = self.view.advice_2.text() if hasattr(self.view, 'advice_2') else ""
            val_tips = self.view.input_tips.toPlainText() if hasattr(self.view, 'input_tips') else ""

            data = {
                "HẠNG MỤC": ["GPA Hiện tại", "Tiến độ học tập", "Số dư tài chính", "Đánh giá tổng quan",
                             "Lời khuyên chi tiết"],
                "KẾT QUẢ": [val_gpa, val_tiendo, val_vitien, val_nhanxet, val_tips]
            }
            return pd.DataFrame(data)
        except Exception as e:
            QMessageBox.critical(self.view.MainWindow, "Lỗi Dữ Liệu", f"Không thể lấy dữ liệu: {e}")
            return None

    def export_to_excel(self):
        try:
            df = self.lay_du_lieu_oversight()
            if df is None: return

            # Tạo tên file
            thoi_gian = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            ten_mac_dinh = f"BaoCao_Oversight_{thoi_gian}.xlsx"
            duong_dan, _ = QFileDialog.getSaveFileName(
                self.view.MainWindow,
                "Lưu file Excel",
                ten_mac_dinh,
                "Excel Files (*.xlsx)"
            )

            if duong_dan:
                df.to_excel(duong_dan, index=False, engine='openpyxl')
                QMessageBox.information(self.view.MainWindow, "Thành công", f"Đã xuất file tại:\n{duong_dan}")

        except ImportError:
            QMessageBox.warning(self.view.MainWindow, "Thiếu thư viện", "Vui lòng cài đặt thư viện: pip install openpyxl")
        except Exception as e:
            QMessageBox.warning(self.view.MainWindow, "Lỗi", f"Không thể xuất file Excel:\n{e}")

    def export_to_csv(self):
        try:
            df = self.lay_du_lieu_oversight()
            if df is None: return

            thoi_gian = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            ten_mac_dinh = f"BaoCao_Oversight_{thoi_gian}.csv"
            duong_dan, _ = QFileDialog.getSaveFileName(
                self.view.MainWindow,
                "Lưu file CSV",
                ten_mac_dinh,
                "CSV Files (*.csv)"
            )

            if duong_dan:
                # utf-8-sig giúp mở trong Excel không bị lỗi font tiếng Việt
                df.to_csv(duong_dan, index=False, encoding='utf-8-sig')
                QMessageBox.information(self.view.MainWindow, "Thành công", f"Đã xuất file tại:\n{duong_dan}")

        except Exception as e:
            QMessageBox.warning(self.view.MainWindow, "Lỗi", f"Không thể xuất file CSV:\n{e}")
# Đóng phần insights }