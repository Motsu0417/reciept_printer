def create_reciept(taget_name, price, specific=None, date_value=None):
    """
    既存のPDFファイルに文字を挿入し、別名で出力します
    :param insert_text:         挿入するテキスト
    :return:
    """
    from pdfrw import PdfReader
    from pdfrw.buildxobj import pagexobj
    from pdfrw.toreportlab import makerl
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    from reportlab.pdfbase import pdfmetrics
    from reportlab.lib.units import mm
    from reportlab.pdfbase.ttfonts import TTFont
    import datetime
    import shutil
    import os

    # 出力名
    output_name = "application/pdfrw.pdf"
    # PDF新規作成
    cc = canvas.Canvas(output_name,pagesize=(145*mm, 54.8*mm))

    # フォントの設定
    font_name = "myfont"
    # pdfmetrics.registerFont(UnicodeCIDFont(font_name))
    pdfmetrics.registerFont(TTFont(font_name,"application/noto_sans.ttf"))

    # 既存ページ読み込み
    page = PdfReader("application/reciept.pdf", decompress=False).pages
    # 1ページ目をオブジェクトに
    pp = pagexobj(page[0])
    cc.doForm(makerl(cc, pp))
    
    price = int(price)

    # 消費税の計算
    tax = int(price / 11)
    print("tax",tax)
    
    # 文字列挿入
    # 宛名
    name_x, name_y = 2*mm, 45   *mm
    cc.setFont(font_name, 9.5)
    cc.drawString(name_x, name_y, taget_name)
    
    # 金額
    price_x, price_y = 80*mm, 37*mm
    cc.setFont(font_name, 14)
    cc.drawString(price_x, price_y, "¥{:,}ー".format(price))
    
    # 消費税
    tax_x, tax_y = 86*mm, 31.9*mm
    cc.setFont(font_name, 9.4)
    cc.drawString(tax_x, tax_y, "{:,}円".format(tax))
    
    # 但し書き
    if specific:
        specific_x, specific_y = 67*mm, 27*mm    
        cc.drawString(specific_x, specific_y, specific)
    
    #　日付記入
    date_x, date_y = 66*mm, 12.3*mm
    if date_value:
        date_value = datetime.datetime.strptime(date_value, "%Y-%m-%d").strftime("%Y年%m月%d日")
        cc.drawString(date_x, date_y, date_value)
    else:
        date_value = datetime.datetime.now().strftime("%Y年%m月%d日")
        cc.drawString(date_x, date_y,date_value)
    
    # 番号記入
    number_x, number_y = 59*mm, 8   *mm
    reciept_folder_path = "reciept_files"
    reciept_number = 1
    date_str_for_file = datetime.datetime.now().strftime("%Y%m%d")
    file_name = ""
    while True:
        reciept_total_num = "{}{:03}".format(date_str_for_file, reciept_number)
        file_name = "{}/{}.pdf".format(reciept_folder_path,reciept_total_num)
        if reciept_number >= 1000:
            raise Exception("file exception: exist limit of file")
        if not os.path.isfile(file_name):
            break
        reciept_number += 1
    
    cc.drawString(number_x, number_y, reciept_total_num)
    
    cc.showPage()
    # 保存
    cc.save()
    
    shutil.copy(output_name, file_name)
    return file_name
    
if __name__ == '__main__':
    file_path = create_reciept("(株)ケイズファクトリー",5500,"ご飲食代")
    print(file_path)