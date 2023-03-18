from PyQt6.QtWidgets import QMainWindow,QApplication,QFileDialog, \
    QMessageBox,QFontDialog,QColorDialog
import sys
from PyQt6.QtGui import QFont
from notepaddemo import Ui_MainWindow
from PyQt6.QtCore import QFileInfo,Qt
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog,QPrintPreviewDialog

class Notepadwindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.actionSave.triggered.connect(self.save_file)
        self.actionNew.triggered.connect(self.file_new)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionPrint.triggered.connect(self.print_file)
        self.actionPrint_Preview.triggered.connect(self.preview_dialog)
        self.actionExport_PDF.triggered.connect(self.export_pdf)
        self.actionQuit.triggered.connect(self.exit_app)
        self.actionBold.triggered.connect(self.text_bold)
        self.actionItalic.triggered.connect(self.text_italic)
        self.actionUnderline.triggered.connect(self.text_underline)
        self.actionLeft.triggered.connect(self.align_left)
        self.actionRight.triggered.connect(self.align_right)
        self.actionCentre.triggered.connect(self.align_centre)
        self.actionJustify.triggered.connect(self.align_justify)
        self.actionFont.triggered.connect(self.font_dialog)
        self.actionColor.triggered.connect(self.color_dialog)
        self.actionAbout_app.triggered.connect(self.about)
        
        ## No need to create function for edit commands/ just connect
        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)

        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionPaste.triggered.connect(self.textEdit.paste)
        



    def save_file(self):
        filename = QFileDialog.getSaveFileName(self,"Save File")

        if filename[0]:
            f = open(filename[0],'w')

            with f:
                text = self.textEdit.toPlainText()
                f.write(text)

                QMessageBox.about(self,"Save File","File has been saved")
     
    def file_new(self):
        if self.edit_save():
            self.textEdit.clear()

    def edit_save(self):
        if not self.textEdit.document().isModified():
            return True

        ret = QMessageBox.warning(self,"Application",
                                  "This document is modified. \n Do you want to save changes ? ",
                                  QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)

        if ret == QMessageBox.StandardButton.Save:
            return self.save_file()

        return ret != QMessageBox.StandardButton.Cancel

    def open_file(self):
        fname = QFileDialog.getOpenFileName(self,"Open File",'/home') 

        if fname[0]:
            f = open(fname[0],'r')

            with f:
                data = f.read()
                self.textEdit.setText(data) 

    def print_file(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer)

        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.textEdit.print(printer)

    def preview_dialog(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        previewDialog = QPrintPreviewDialog(printer,self)
        previewDialog.paintRequested.connect(self.print_preview)
        previewDialog.exec()

    def print_preview(self,printer):
        self.textEdit.print(printer)

    def export_pdf(self):
        fn,_= QFileDialog.getSaveFileName(self,'Export PDF',"PDF files (.pdf) ;; All Files()")

        if fn != "" and QFileInfo(fn).suffix() == "":
            fn += '.pdf'
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(fn)
        self.textEdit.document().print(printer)

    def exit_app(self):
        self.close()

    def text_bold(self):
        font = QFont()
        font.setBold(True)
        self.textEdit.setFont(font)

    def text_italic(self):
        font = QFont()
        font.setItalic(True)
        self.textEdit.setFont(font)

    def text_underline(self):
        font = QFont()
        font.setUnderline(True)
        self.textEdit.setFont(font)

    def align_left(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def align_centre(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def align_right(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignRight)

    def align_justify(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignJustify)

    def font_dialog(self):
        font,ok = QFontDialog.getFont()

        if ok:
            self.textEdit.setFont(font)

    def color_dialog(self):
        color =  QColorDialog.getColor()
        self.textEdit.setTextColor(color)

    def about(self):
        QMessageBox.about(self, "About App","This is a simple Notepad Application with PyQt6")

    

app = QApplication(sys.argv)
Note = Notepadwindow()
sys.exit(app.exec())
