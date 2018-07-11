
import xlsxwriter

import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select

driver = webdriver.Chrome('D:\\classTutorial\\upworkscrape\\chromedriver.exe')

driver.get("https://www.infomex.org.mx/gobiernofederal/moduloPublico/moduloPublico.action")
driver.maximize_window()

# First dropdown dependencia
objDependencia = Select(driver.find_element_by_name("selectDependencia"))
objDependencia.select_by_index(21)

# Fecha de respuesta
driver.find_element_by_id("fechaRespuestaDesdeS").send_keys("01/01/2016")
driver.find_element_by_id("fechaRespuestaHastaS").send_keys("28/06/2018")

# Tipo de respuesta
objTipo = Select(driver.find_element_by_id("selectTipoRespuestaS"))
objTipo.select_by_index(1)

# Estatus
objEsta = Select(driver.find_element_by_name("selectEstatusS"))
objEsta.select_by_index(11)

# Buscar click
driver.find_element_by_id("buttonBuscarS").click()
# wait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_xpath("//iframe[@id='iReports']")))
Matrix = []

Matrix.append("Folio de la Solicitud")
Matrix.append("Fecha de Recepción")
Matrix.append("Unidad de Información")
Matrix.append("Respuesta")
Matrix.append("Fecha de Respuesta")
Matrix.append("Recurso de revisión (en caso de tener)")
# jumping to iframe

# picking frames
index = 6
for i in range(22):
    driver.switch_to.default_content()
    frames = driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(frames[0])
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all('div', attrs={'style': 'WIDTH:100%;overflow-x:hidden'}):
        if not (tag.text == "Folio de la Solicitud" or tag.text == "Fecha de Recepción" or tag.text == "Unidad de Información" or tag.text == "Respuesta" or tag.text == "Fecha de Respuesta" or tag.text == "Recurso de revisión (en caso de tener)"):
            Matrix.append(tag.text)
            index += 1
    driver.find_element_by_name("rptVisor$ctl01$ctl01$ctl05$ctl00$ctl00").click()
    time.sleep(3)

#driver.close()

# xls writer
workbook = xlsxwriter.Workbook('datascrape.xlsm')
worksheet = workbook.add_worksheet()





worksheet.write(0, 0, Matrix[0])
worksheet.write(0, 1, Matrix[1])
worksheet.write(0, 2, Matrix[2])
worksheet.write(0, 3, Matrix[3])
worksheet.write(0, 4, Matrix[4])
worksheet.write(0, 5, Matrix[5])
sayac = 0
while sayac < len(Matrix):
    print(Matrix[sayac])
    sayac += 1
# WRITE TO FILE
# file = open("datascrape.txt","w")
linecount = 0
count = 6
row = 1
column = 0
i = 0
while count < len(Matrix):
    if column<5:
        print(Matrix[count])
        worksheet.write(row, column, Matrix[count])
        column += 1
        count += 1

    else:
        linecount += 1
        worksheet.write(row, column, " ")
        row += 1
        column = 0
print(linecount)

workbook.close()
