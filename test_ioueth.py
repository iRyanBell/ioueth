import pytest
import logging

log = logging.getLogger().info

@pytest.fixture
def contract(w3, get_contract):
	with open('./ioueth.vy') as f:
		contract_code = f.read()
	return get_contract(contract_code)

def test_initial_balances(w3, contract):
	k0 = w3.eth.accounts[0]
	k1 = w3.eth.accounts[1]

	# The initial balances should be zero.
	assert contract.iou_balance(k0, k1) == 0
	assert contract.iou_balance(k1, k0) == 0

def test_iou(w3, contract):
	k0 = w3.eth.accounts[0]
	k1 = w3.eth.accounts[1]
	k2 = w3.eth.accounts[2]

	# Send 1/2 IOU from k0 -> k1
	contract.iou(k1, transact={'from': k0})
	assert contract.iou_balance(k0, k1) == 1
	assert contract.iou_balance(k1, k0) == -1

	# Send IOU from k1 -> k2
	contract.iou(k2, transact={'from': k1})
	assert contract.iou_balance(k1, k2) == 1
	assert contract.iou_balance(k2, k1) == -1

	# Send 2/2 IOU from k0 -> k1
	contract.iou(k1, transact={'from': k0})
	assert contract.iou_balance(k0, k1) == 2
	assert contract.iou_balance(k1, k0) == -2

	# Reverse 1/2 IOU with k1 -> k0
	contract.iou(k0, transact={'from': k1})
	assert contract.iou_balance(k0, k1) == 1
	assert contract.iou_balance(k1, k0) == -1

	# Reverse 2/2 IOU with k1 -> k0
	contract.iou(k0, transact={'from': k1})
	assert contract.iou_balance(k0, k1) == 0
	assert contract.iou_balance(k1, k0) == 0

	# Reverse IOU from k2 -> k1
	contract.iou(k1, transact={'from': k2})
	assert contract.iou_balance(k1, k2) == 0
	assert contract.iou_balance(k2, k1) == 0

def test_logs(w3, contract, get_logs):
	k0 = w3.eth.accounts[0]
	k1 = w3.eth.accounts[1]

	# Send IOU from k1 -> k0
	tx = contract.iou(k0, transact={'from': k1})
	evt = get_logs(tx, contract, 'Iou')[0]

	assert evt['event'] == 'Iou'
	assert evt['args']['_from'] == k1
	assert evt['args']['_to'] == k0