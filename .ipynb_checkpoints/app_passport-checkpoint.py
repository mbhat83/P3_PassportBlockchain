
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/passport_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()

# set the title and sidebar
st.set_page_config(page_title="TravelLog", page_icon=":airplane:", layout="wide")
st.sidebar.title("TravelLog Smart Contract")
st.sidebar.write("Enter the details of the travel record to add:")

# get the input from the user
passportID = st.sidebar.text_input("Passport ID")
passportExpirationDate = st.sidebar.date_input("Passport Expiration Date")
fullName = st.sidebar.text_input("Full Name")
countryOfResidence = st.sidebar.text_input("Country of Residence")
countryOfOrigin = st.sidebar.text_input("Country of Origin")
destinationCountry = st.sidebar.text_input("Destination Country")
entryDate = st.sidebar.date_input("Entry Date")
plannedExitDate = st.sidebar.date_input("Planned Exit Date")

# add the travel record to the blockchain
if st.sidebar.button("Add Travel Record"):
    response = add_travel_record(passportID, int(passportExpirationDate.timestamp()), fullName, countryOfResidence, countryOfOrigin, destinationCountry, int(entryDate.timestamp()), int(plannedExitDate.timestamp()))
    st.sidebar.write(response)

# set the main content area
st.title("TravelLog Smart Contract")
st.write("This smart contract allows you to add, update, and view travel records.")
st.write("Enter the passport ID and entry date of the travel record to view:")

# get the input from the user
passportID = st.text_input("Passport ID")
entryDate = st.date_input("Entry Date")

# get the travel record from the blockchain
if st.button("Get Travel Record"):
    response = get_travel_record(passportID, int(entryDate.timestamp()))
    st.write(response)
    
# update the travel record in the blockchain
exitDate = st.date_input("Exit Date")
if st.button("Update Travel Record"):
    response = update_travel_record(passportID, int(exitDate.timestamp()))
    st.write(response)


   
