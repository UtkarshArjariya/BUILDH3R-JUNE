from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams, 
)

algorand = AlgorandClient.default_local_net()
dispenser = algorand.account.dispenser()
print("Dispenser: ", dispenser.address)
creator = algorand.account.random()
print("Creator: ", creator.address)

algorand.send_payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000,
    )
)

sent_txn = algorand.send_asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=50,
        asset_name="BUILDH3R",
        unit_name="HER",
        manager=creator.address,
        clawback=creator.address,
        freeze=creator.address
    )
)

asset_id = sent_txn['confirmation']['asset-index']
print("Asset ID: ", asset_id)

# Receiver A
receiver_acct = algorand.account.random()
print("Receiver A Acc: ", receiver_acct.address)
# Fund the receiver account
algorand.send_payment(
    PayParams(
        sender=dispenser.address,
        receiver=receiver_acct.address,
        amount=10_000_000,
    )
)

group_txn = algorand.new_group()
# Opt in to select the asset to prevent Spam
group_txn.add_asset_opt_in(
    AssetOptInParams(
        sender=receiver_acct.address,
        asset_id=asset_id,
    )
)

group_txn.add_payment(PayParams(
    sender=receiver_acct.address,
    receiver=creator.address,
    amount=1_000_000,
))

group_txn.add_asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=receiver_acct.address,
        asset_id=asset_id,
        amount=10
    )
)

group_txn.execute(algorand)

print("Before Clawback Receiver Account Asset Balance", algorand.account.get_information(receiver_acct.address)["assets"][0]['amount'])
print("Before Clawback Creator Account Asset Balance", algorand.account.get_information(creator.address)["assets"][0]['amount'])

algorand.send_asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        asset_id=asset_id,
        amount=10,
        receiver=creator.address,
        clawback_target=receiver_acct.address
    )
)

print("After Clawback Receiver Account Asset Balance", algorand.account.get_information(receiver_acct.address)["assets"][0]['amount'])
print("After Clawback Creator Account Asset Balance", algorand.account.get_information(creator.address)["assets"][0]['amount'])
