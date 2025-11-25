// export/excel.ts
import ExcelJS from 'exceljs'
import { format } from 'date-fns'

export const generateExcel = async (takeoff: any, pricing: any) => {
  const workbook = new ExcelJS.Workbook()
  const sheet = workbook.addWorksheet('Takeoff')
  
  sheet.addRow(['TAKEOFF TURBO – SOVEREIGN EDITION'])
  sheet.addRow([`Project: \( {takeoff.project_name}`, `Date: \){format(new Date(), 'PP')}`])
  sheet.addRow([])
  sheet.addRow(['Item', 'Description', 'Qty', 'Unit', 'Material', 'Unit Price', 'Total'])
  
  takeoff.items.forEach(item => {
    const price = pricing.find(p => p.material.includes(item.material_spec))?.price || 0
    sheet.addRow([
      item.section,
      item.description,
      item.quantity,
      item.unit,
      item.material_spec,
      price,
      item.quantity * price
    ])
  })
  
  const buffer = await workbook.xlsx.writeBuffer()
  return buffer
}