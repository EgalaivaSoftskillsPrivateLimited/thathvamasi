/**
 * Thathvamasi HR Consultancy (THC) - CSV Export Utility
 */

export function exportToCSV(filename, headers, rows) {
  if (!rows || !rows.length) return false;

  const csvRows = [
    headers.join(','),
    ...rows.map(row => 
      row.map(val => {
        const str = String(val ?? '').replace(/"/g, '""');
        return `"${str}"`;
      }).join(',')
    )
  ];

  const blob = new Blob([csvRows.join('\n')], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', `${filename}_${new Date().toISOString().split('T')[0]}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  return true;
}
