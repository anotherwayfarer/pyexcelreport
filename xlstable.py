#!/usr/bin/python
# -*- coding: utf-8 -*-

from xlsutils_apply import *

class XLSTableColumnInfo:
    """Структура для хранения информации одного столбца данных таблицы
    """
    def __init__(self, fieldname, type = 'string', xlscolumns=1):
        self.fieldname  = fieldname
        self.xlscolumns = xlscolumns

class XLSTable:
    """Класс, инкапсулирующий информацию и методы отображения данных таблицы
    """
    def __init__(self, colinfo, data):
        self._colinfo = colinfo
        self._data = data
        self._col_count = sum(hdr.xlscolumns for hdr in colinfo)
        self._row_count = len(data)

    def column_count(self):
        """Возвращает количество физических столбцов в таблице
        """
        return self._col_count

    def apply(self, ws, first_row, first_col):
        """Отображает непосредственно в XLS данные таблицы
        """
        cur_row = first_row
        for row in self._data:
            ws.row_dimensions[cur_row].height = 30

            cur_col = first_col
            col_index = 0
            for coli in self._colinfo:
                if coli.xlscolumns > 1:
                    ws.merge_cells(start_row=cur_row, start_column=cur_col, \
                                   end_row=cur_row,   end_column=cur_col + coli.xlscolumns - 1)

                ws.cell(row=cur_row, column=cur_col).value = row[col_index]
                cur_col += coli.xlscolumns
                col_index += 1
            cur_row += 1

        range = CellRange(min_row=first_row, min_col=first_col, \
                          max_row=cur_row - 1, max_col=cur_col - 1)
        apply_xlrange(ws, range, set_borders)
        apply_xlrange(ws, range, set_outline, border_style='medium')
        apply_xlrange(ws, range, set_font)
        apply_xlrange(ws, range, set_alignment)
