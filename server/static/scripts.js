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
				anchor.href = 'receipt/'+ receipt.id
				const receiptBox = document.createElement('div');
				receiptBox.className = 'box'

				const storeName = document.createElement('p')
				storeName.textContent = receipt.store.toUpperCase()
				storeName.className = 'store-name'

				const date = document.createElement('p')
				date.textContent = receipt.date
				date.className = 'date'

				const address = document.createElement('p')
				address.textContent = receipt.address
				address.className = 'address'

				const itemsContainer = document.createElement('div')

				const itemsArray = receipt.items
				itemsArray.forEach(item => {
					const items = document.createElement('div')
					items.className = 'items'
					const itemName = document.createElement('p')
					itemName.className = 'item-name'
					const itemPrice = document.createElement('p')
					itemPrice.className = 'item-price'
					const itemQuantity = document.createElement('p')
					itemQuantity.className = 'item-quantity'
					itemName.textContent = item.name
					itemPrice.textContent = '$' + item.price
					itemQuantity.textContent = item.quantity

					items.appendChild(itemName)
					items.appendChild(itemQuantity)
					items.appendChild(itemPrice)

					itemsContainer.appendChild(items)
				})


				const total = document.createElement('p')
				total.textContent = receipt.total
				total.className = 'total'

				receiptBox.appendChild(storeName)
				receiptBox.appendChild(address)
				receiptBox.appendChild(date)
				receiptBox.appendChild(itemsContainer)
				receiptBox.appendChild(total)

				address.textContent = receipt.address
				address.className = 'address'

				skinPattern(receiptBox)
				let cells = [receipt.id, receipt.date, receipt.items, receipt.total, receipt.store, receipt.address, receipt.phone, receipt.payment_method];
				anchor.appendChild(receiptBox);
				receiptsGrid.appendChild(anchor);
			});
		});
}
document.addEventListener('DOMContentLoaded', getAllReceipts);

