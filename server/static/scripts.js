function skinPattern(receiptBox) {
	const xCoord = Math.floor(Math.random() * -1033);
	const yCoord = Math.floor(Math.random() * -500);
	receiptBox.style.backgroundPosition = `${xCoord}px ${yCoord}px`;
}

function getAllReceipts() {
	fetch('http://localhost:5000/api/get_all_receipts')
		.then(res => res.json())
		.then(data => {
			console.log(data);
			const receiptsGrid = document.querySelector('.receipts-grid');

			data.forEach(receipt => {
				const anchor = document.createElement('a');
				anchor.href = "https://youtube.com"
				const receiptBox = document.createElement('div');
				receiptBox.textContent = receipt.store
				receiptBox.className = 'box'
				skinPattern(receiptBox)
				let cells = [receipt.id, receipt.date, receipt.items, receipt.total, receipt.store, receipt.address, receipt.phone, receipt.payment_method];
				anchor.appendChild(receiptBox);
				receiptsGrid.appendChild(anchor);
			});
		});
}
document.addEventListener('DOMContentLoaded', getAllReceipts);