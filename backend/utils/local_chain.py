### Script to run a local blockchain and set up the Subscriptions contract
from os import getcwd
from subprocess import call
from shutil import move


def start_chain():
    # Binance fork... Can be any blockchain
    call("ganache-cli --fork https://data-seed-prebsc-1-s1.binance.org:8545", shell=True)


def deploy_contract():
    # The path to the SubscriptionsModel.
    # Change if neccessary
    path_to_project = f"{getcwd()}/../../Solidity_Projects/SubscriptionsModel"
    # Run the subscribe script
    call(f"cd {path_to_project} && brownie run subscribe --network bsc-main-fork", shell=True)
    # Now move generated json file to this directory 
    move(f"{getcwd()}/../../Solidity_Projects/SubscriptionsModel/contract.json", "contract.json")


if __name__ == "__main__":
    # I don't suggesst calling this... 
    # Instead you should just copy and paste ganache-cli --fork https://data-seed-prebsc-1-s1.binance.org:8545 
    # into your terminal
    # start_chain()

    # This you should call!
    deploy_contract()