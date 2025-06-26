function getAllReceipts() {
	fetch('http://localhost:5000/api/get_all_receipts')
		.then(res => res.json())
		.then(data => {
			const tableBody = document.querySelector('#all-receipts tbody');

			data.forEach(receipt => {
				const row = document.createElement('tr');
				let cells = [receipt.id, receipt.item, receipt.store, receipt.price, receipt.date];
				cells.forEach(cellData => {
					let td = document.createElement('td');
					td.textContent = cellData;
					row.appendChild(td);
				});
				tableBody.appendChild(row);
			});
		});
}
document.addEventListener('DOMContentLoaded', getAllReceipts);