import pytest
import logging

log = logging.getLogger().info

@pytest.fixture
def ioueth_contract(w3, get_contract):
	with open('./ioueth.vy') as f:
		contract_code = f.read()
	return get_contract(contract_code)

def test_initial_balances(w3, ioueth_contract):
	k0 = w3.eth.accounts[0]
	k1 = w3.eth.accounts[1]

	# The initial balances should be zero.
	assert ioueth_contract.iou_balance(k0, k1) == 0
	assert ioueth_contract.iou_balance(k1, k0) == 0

def test_iou(w3, ioueth_contract):
	k0 = w3.eth.accounts[0]
	k1 = w3.eth.accounts[1]
	k2 = w3.eth.accounts[2]

	# Send 1/2 IOU from k0 -> k1
	ioueth_contract.iou(k1, transact={"from": k0})
	assert ioueth_contract.iou_balance(k0, k1) == 1
	assert ioueth_contract.iou_balance(k1, k0) == -1

	# Send 1/1 IOU from k1 -> k2
	ioueth_contract.iou(k2, transact={"from": k1})
	assert ioueth_contract.iou_balance(k1, k2) == 1
	assert ioueth_contract.iou_balance(k2, k1) == -1

	# Send 2/2 IOU from k0 -> k1
	ioueth_contract.iou(k1, transact={"from": k0})
	assert ioueth_contract.iou_balance(k0, k1) == 2
	assert ioueth_contract.iou_balance(k1, k0) == -2

	# Reverse 1/2 IOU with k1 -> k0
	ioueth_contract.iou(k0, transact={"from": k1})
	assert ioueth_contract.iou_balance(k0, k1) == 1
	assert ioueth_contract.iou_balance(k1, k0) == -1

	# Reverse 2/2 IOU with k1 -> k0
	ioueth_contract.iou(k0, transact={"from": k1})
	assert ioueth_contract.iou_balance(k0, k1) == 0
	assert ioueth_contract.iou_balance(k1, k0) == 0

	# Reverse 1/1 IOU from k2 -> k1
	ioueth_contract.iou(k1, transact={"from": k2})
	assert ioueth_contract.iou_balance(k1, k2) == 0
	assert ioueth_contract.iou_balance(k2, k1) == 0