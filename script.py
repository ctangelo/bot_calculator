import xlwings as xw


def receive_data_and_make_pdf(source_file_name, user_id):

    # Открываем документ со сметой
    target_wb = xw.Book('/root/doc/calculation.xlsx', update_links=False)
    current_sheet = target_wb.sheets['Ввод']

    # Открываем документ от менеджера
    source_wb = xw.Book(source_file_name, update_links=False)
    data_sheet = source_wb.sheets['Ввод']

    # Определяем область данных на листе "Ввод" от менеджера, и копируем ее
    data_range = data_sheet.used_range
    data_range.api.Copy()

    # Вставляем данные с настройками форматирования на вкладку "Ввод" документа со сметой. Сохраняем файл.
    current_sheet.range('A1').api.PasteSpecial()
    target_wb.save()

    # -----------------Сохранение сметы в PDF---------------

    # Выбираем вкладку и диапазон ячеек для сохранения в PDF. Выполняем автоподгонку по высоте ячеек.
    cell_range = target_wb.sheets['Смета']['C1:L580']
    cell_range.rows.autofit()

    # Создаем путь и имя файла PDF
    pdf_file_path = f"/root/doc/{user_id}/Смета"

    # Сохраняем указанный диапазон ячеек в PDF
    cell_range.to_pdf(pdf_file_path)

    # Закрываем оба документа
    source_wb.close()
    target_wb.close()
