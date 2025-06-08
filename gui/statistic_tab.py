import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from db import get_connection
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
from datetime import datetime
import tempfile
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class StatisticTab:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(master)
        self.frame.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        self.day_btn = ttk.Button(btn_frame, text='Doanh thu ngày', style='Accent.TButton', command=self.show_day)
        self.day_btn.pack(side='left', padx=5)
        self.month_btn = ttk.Button(btn_frame, text='Doanh thu tháng', style='Accent.TButton', command=self.show_month)
        self.month_btn.pack(side='left', padx=5)
        self.top_btn = ttk.Button(btn_frame, text='Sản phẩm bán chạy', style='Accent.TButton', command=self.show_top)
        self.top_btn.pack(side='left', padx=5)
        self.export_btn = ttk.Button(btn_frame, text='Xuất báo cáo PDF', style='Accent.TButton', command=self.export_report)
        self.export_btn.pack(side='left', padx=5)
        self.canvas_frame = ttk.Frame(self.frame)
        self.canvas_frame.pack(fill='both', expand=True, padx=10, pady=10)

    def show_day(self):
        self._show_revenue_chart('DAY')

    def show_month(self):
        self._show_revenue_chart('MONTH')

    def show_top(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''SELECT p.Name, SUM(d.Quantity) as total_qty 
                              FROM InvoiceDetails d JOIN Products p ON d.ProductId = p.id 
                              GROUP BY d.ProductId ORDER BY total_qty DESC LIMIT 5''')
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            names = [row[0] for row in data]
            qtys = [row[1] for row in data]
            fig, ax = plt.subplots(figsize=(5,3))
            ax.bar(names, qtys)
            ax.set_title('Top 5 sản phẩm bán chạy')
            ax.set_ylabel('Số lượng')
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi thống kê: {e}')

    def _show_revenue_chart(self, mode):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        try:
            conn = get_connection()
            cursor = conn.cursor()
            if mode == 'DAY':
                cursor.execute("""SELECT DATE(CreateAt), SUM(Amount) FROM Invoices GROUP BY DATE(CreateAt)""")
            else:
                cursor.execute("""SELECT DATE_FORMAT(CreateAt, '%Y-%m'), SUM(Amount) FROM Invoices GROUP BY DATE_FORMAT(CreateAt, '%Y-%m')""")
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            labels = [str(row[0]) for row in data]
            values = [row[1] for row in data]
            fig, ax = plt.subplots(figsize=(5,3))
            ax.plot(labels, values, marker='o')
            ax.set_title('Doanh thu theo ' + ('ngày' if mode=='DAY' else 'tháng'))
            ax.set_ylabel('Doanh thu')
            ax.set_xticklabels(labels, rotation=45)
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi thống kê: {e}')

    def export_report(self):
        """Xuất báo cáo thống kê ra file PDF"""
        try:
            # Đăng ký font Unicode hỗ trợ tiếng Việt
            font_path = os.path.join('utils', 'DejaVuSans.ttf')
            pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
            
            # Chọn nơi lưu file
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Lưu báo cáo thống kê"
            )
            
            if not file_path:
                return
            
            # Tạo document PDF
            doc = SimpleDocTemplate(file_path, pagesize=A4)
            story = []
            
            # Thiết lập styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontName='DejaVuSans',
                fontSize=18,
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontName='DejaVuSans',
                fontSize=14,
                spaceAfter=12,
                alignment=TA_LEFT
            )
            
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontName='DejaVuSans',
            )
            
            # Tiêu đề báo cáo
            title = Paragraph("BÁO CÁO THỐNG KÊ CỬA HÀNG HOA", title_style)
            story.append(title)
            
            # Thời gian tạo báo cáo
            current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            time_para = Paragraph(f"Thời gian tạo báo cáo: {current_time}", normal_style)
            story.append(time_para)
            story.append(Spacer(1, 20))
            
            # 1. Báo cáo doanh thu theo ngày
            story.append(Paragraph("1. DOANH THU THEO NGÀY", heading_style))
            daily_data = self._get_daily_revenue()
            if daily_data:
                daily_table_data = [['Ngày', 'Doanh thu (VNĐ)']]
                total_daily = 0
                for row in daily_data:
                    daily_table_data.append([str(row[0]), f"{row[1]:,.0f}"])
                    total_daily += row[1]
                daily_table_data.append(['TỔNG CỘNG', f"{total_daily:,.0f}"])
                
                daily_table = Table(daily_table_data)
                daily_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                    ('FONTNAME', (0, -1), (-1, -1), 'DejaVuSans'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(daily_table)
            else:
                story.append(Paragraph("Không có dữ liệu doanh thu theo ngày", styles['Normal']))
            
            story.append(Spacer(1, 20))
            
            # 2. Báo cáo doanh thu theo tháng
            story.append(Paragraph("2. DOANH THU THEO THÁNG", heading_style))
            monthly_data = self._get_monthly_revenue()
            if monthly_data:
                monthly_table_data = [['Tháng', 'Doanh thu (VNĐ)']]
                total_monthly = 0
                for row in monthly_data:
                    monthly_table_data.append([str(row[0]), f"{row[1]:,.0f}"])
                    total_monthly += row[1]
                monthly_table_data.append(['TỔNG CỘNG', f"{total_monthly:,.0f}"])
                
                monthly_table = Table(monthly_table_data)
                monthly_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                    ('FONTNAME', (0, -1), (-1, -1), 'DejaVuSans'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(monthly_table)
            else:
                story.append(Paragraph("Không có dữ liệu doanh thu theo tháng", styles['Normal']))
            
            story.append(Spacer(1, 20))
            
            # 3. Top sản phẩm bán chạy
            story.append(Paragraph("3. TOP 10 SẢN PHẨM BÁN CHẠY", heading_style))
            top_products = self._get_top_products()
            if top_products:
                product_table_data = [['STT', 'Tên sản phẩm', 'Số lượng bán', 'Doanh thu (VNĐ)']]
                for i, row in enumerate(top_products, 1):
                    product_table_data.append([
                        str(i), 
                        row[0], 
                        str(row[1]), 
                        f"{row[2]:,.0f}" if row[2] else "0"
                    ])
                
                product_table = Table(product_table_data)
                product_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(product_table)
            else:
                story.append(Paragraph("Không có dữ liệu sản phẩm bán chạy", styles['Normal']))
            
            # Thêm thống kê tổng quan
            story.append(Spacer(1, 20))
            story.append(Paragraph("4. THỐNG KÊ TỔNG QUAN", heading_style))
            # Tổng quan về đơn hàng
            general_stats = self._get_general_statistics()
            if general_stats and len(general_stats) > 0:
                stats_table_data = [['Chỉ số', 'Giá trị']]
                for stat in general_stats:
                    stats_table_data.append([stat[0], stat[1]])
                stats_table = Table(stats_table_data)
                stats_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(stats_table)
            else:
                story.append(Paragraph("Không có dữ liệu thống kê tổng quan", normal_style))
            
            # Tạo file PDF
            doc.build(story)
            
            messagebox.showinfo('Thành công', f'Đã xuất báo cáo thành công!\nFile được lưu tại: {file_path}')
            
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi khi xuất báo cáo: {str(e)}')
    
    def _get_daily_revenue(self):
        """Lấy dữ liệu doanh thu theo ngày"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DATE(CreateAt) as date, SUM(Amount) as revenue 
                FROM Invoices 
                GROUP BY DATE(CreateAt) 
                ORDER BY date DESC
                LIMIT 30
            """)
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            return data
        except Exception:
            return []
    
    def _get_monthly_revenue(self):
        """Lấy dữ liệu doanh thu theo tháng"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DATE_FORMAT(CreateAt, '%Y-%m') as month, SUM(Amount) as revenue 
                FROM Invoices 
                GROUP BY DATE_FORMAT(CreateAt, '%Y-%m') 
                ORDER BY month DESC
                LIMIT 12
            """)
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            return data
        except Exception:
            return []
    
    def _get_top_products(self):
        """Lấy dữ liệu top sản phẩm bán chạy"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.Name, SUM(d.Quantity) as total_qty, SUM(d.Quantity * d.Price) as revenue
                FROM InvoiceDetails d 
                JOIN Products p ON d.ProductId = p.id 
                GROUP BY d.ProductId, p.Name 
                ORDER BY total_qty DESC 
                LIMIT 10
            """)
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            return data
        except Exception:
            return []
    
    def _get_general_statistics(self):
        """Lấy thống kê tổng quan"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            stats = []
            
            # Tổng số đơn hàng
            cursor.execute("SELECT COUNT(*) FROM Invoices")
            total_invoices = cursor.fetchone()[0]
            stats.append(['Tổng số đơn hàng', f"{total_invoices:,}"])
            
            # Tổng doanh thu
            cursor.execute("SELECT SUM(Amount) FROM Invoices")
            total_revenue = cursor.fetchone()[0] or 0
            stats.append(['Tổng doanh thu', f"{total_revenue:,.0f} VNĐ"])
            
            # Tổng số sản phẩm đã bán
            cursor.execute("SELECT SUM(Quantity) FROM InvoiceDetails")
            total_products_sold = cursor.fetchone()[0] or 0
            stats.append(['Tổng số sản phẩm đã bán', f"{total_products_sold:,}"])
            
            # Đơn hàng trung bình
            if total_invoices > 0:
                avg_order = total_revenue / total_invoices
                stats.append(['Giá trị đơn hàng trung bình', f"{avg_order:,.0f} VNĐ"])
            
            # Tổng số khách hàng
            cursor.execute("SELECT COUNT(DISTINCT CustomerId) FROM Invoices WHERE CustomerId IS NOT NULL")
            total_customers = cursor.fetchone()[0] or 0
            stats.append(['Tổng số khách hàng', f"{total_customers:,}"])
            
            cursor.close()
            conn.close()
            return stats
        except Exception:
            return []
