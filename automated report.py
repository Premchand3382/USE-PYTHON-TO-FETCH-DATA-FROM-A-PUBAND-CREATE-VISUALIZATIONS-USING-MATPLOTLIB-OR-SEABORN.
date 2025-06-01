# -*- coding: utf-8 -*-
"""
Created on Sun Jun  1 16:45:46 2025

@author: premc
"""

import csv
import statistics
import os
import matplotlib.pyplot as plt
from collections import Counter
from fpdf import FPDF

def read_csv(file_path):
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data, reader.fieldnames if data else []

def analyze_data(data, fieldnames):
    analysis = {}
    analysis['num_records'] = len(data)
    analysis['num_fields'] = len(fieldnames)
    numeric_fields = []
    categorical_fields = []

    for field in fieldnames:
        for row in data:
            try:
                float(row[field])
                numeric_fields.append(field)
                break
            except (ValueError, TypeError):
                if field not in categorical_fields:
                    categorical_fields.append(field)
                break

    stats = {}
    for field in numeric_fields:
        try:
            values = [float(row[field]) for row in data if row[field] != '']
            if values:
                stats[field] = {
                    'mean': round(statistics.mean(values), 2),
                    'median': round(statistics.median(values), 2),
                    'stdev': round(statistics.stdev(values), 2) if len(values) > 1 else 0.0,
                    'min': round(min(values), 2),
                    'max': round(max(values), 2),
                }
        except Exception as e:
            stats[field] = {'error': str(e)}

    cat_stats = {}
    for field in categorical_fields:
        try:
            values = [row[field] for row in data if row[field]]
            if values:
                freq = Counter(values)
                most_common = freq.most_common(1)[0]
                cat_stats[field] = {
                    'unique': len(freq),
                    'most_common': f"{most_common[0]} ({most_common[1]} times)"
                }
        except Exception as e:
            cat_stats[field] = {'error': str(e)}

    analysis['numeric_stats'] = stats
    analysis['categorical_stats'] = cat_stats
    return analysis

def plot_numeric_means(stats, output_img='mean_chart.png'):
    fields = list(stats.keys())
    means = [stats[f]['mean'] for f in fields if 'mean' in stats[f]]

    if not fields or not means:
        return None

    plt.figure(figsize=(8, 4))
    plt.bar(fields, means, color='skyblue')
    plt.title('Mean Values of Numeric Fields')
    plt.xlabel('Field')
    plt.ylabel('Mean')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_img)
    plt.close()
    return output_img

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, self.title, border=False, ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 13)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 8, body)
        self.ln()

    def add_analysis(self, analysis):
        self.chapter_title('Summary')
        summary = (
            f"Number of records: {analysis['num_records']}\n"
            f"Number of fields: {analysis['num_fields']}\n"
        )
        self.chapter_body(summary)

        if analysis['numeric_stats']:
            self.chapter_title('Numeric Field Statistics')
            for field, stat in analysis['numeric_stats'].items():
                if 'error' in stat:
                    stat_text = f"{field}: Error - {stat['error']}"
                else:
                    stat_text = (
                        f"{field}:\n"
                        f"  - Mean: {stat['mean']}\n"
                        f"  - Median: {stat['median']}\n"
                        f"  - Std Dev: {stat['stdev']}\n"
                        f"  - Min: {stat['min']}, Max: {stat['max']}\n"
                    )
                self.chapter_body(stat_text)

        if analysis['categorical_stats']:
            self.chapter_title('Categorical Field Summaries')
            for field, stat in analysis['categorical_stats'].items():
                if 'error' in stat:
                    cat_text = f"{field}: Error - {stat['error']}"
                else:
                    cat_text = (
                        f"{field}:\n"
                        f"  - Unique values: {stat['unique']}\n"
                        f"  - Most common: {stat['most_common']}\n"
                    )
                self.chapter_body(cat_text)

    def add_image(self, img_path):
        if os.path.exists(img_path):
            self.add_page()
            self.chapter_title("Chart: Mean Values")
            self.image(img_path, x=15, y=None, w=180)

def generate_pdf_report(file_path, analysis, report_title, output_path='report.pdf'):
    chart_path = plot_numeric_means(analysis['numeric_stats'])

    pdf = PDFReport()
    pdf.title = report_title
    pdf.add_page()
    pdf.add_analysis(analysis)

    if chart_path:
        pdf.add_image(chart_path)

    pdf.output(output_path)
    print(f"✅ Report generated and saved to: {output_path}")

def main():
    # 👇 Change this to your actual CSV path
    file_path = r"C:\Users\premc\Downloads\customers-100.csv"
    
    # 👇 Desired PDF output path
    output_path = r"C:/Users/premc/OneDrive/Documents/data_analysis_report.pdf"
    
    # 👇 Title shown on top of the PDF
    report_title = "Data Analysis Report"

    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    try:
        data, fieldnames = read_csv(file_path)
        if not data:
            print("❌ No data found in the file.")
            return
        analysis = analyze_data(data, fieldnames)
        generate_pdf_report(file_path, analysis, report_title, output_path)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
