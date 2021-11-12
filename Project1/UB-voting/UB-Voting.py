"""
Project: "UB-Voting"
Description: A simple e-voting application using Blockchain Technology

Author: Sereysathia Luy
Advisor: Omar Abuzaghleh
"""

#importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

# Part 1 - Building a Blockchain
class Blockchain:
    
    #__init__ function called when Blockchain is initialized 
    def __init__(self):
        self.chain = []
        self.votes = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()
        # Store a list voter information to verify vote
        self.voter_data = [ {'Firstname': 'Jules',
                            'Lastname': 'Winnfield',
                            'date of birth': '05/08/1980',
                            'gender': 'male',
                            'voterID': 'QT1994ZBM2'
                            },
                            {'Firstname': 'Ellen',
                            'Lastname': 'Ripley',
                            'date of birth': '02/15/1970',
                            'gender': 'female',
                            'voterID': 'A1975ZNOMP'
                            },
                            {'Firstname': 'Walter',
                            'Lastname': 'White',
                            'date of birth': '01/08/1975',
                            'gender': 'male',
                            'voterID': 'BB10208DBZ'
                            },
                            {'Firstname': 'Selena',
                            'Lastname': 'Kyles',
                            'date of birth': '02/14/1985',
                            'gender': 'female',
                            'voterID': '1940DCTY4Z'
                            },
                            {'Firstname': 'Alyx',
                            'Lastname': 'Vance',
                            'date of birth': '09/09/1997',
                            'gender': 'female',
                            'voterID': 'HL3C2020E3'
                            },
                            {'Firstname': 'Homer',
                            'Lastname': 'Simpson',
                            'date of birth': '12/01/1980',
                            'gender': 'male',
                            'voterID': '22TSSPDT45'
                            },
                            {'Firstname': 'Monica',
                            'Lastname': 'Geller',
                            'date of birth': '01/01/1995',
                            'gender': 'female',
                            'voterID': 'FR47IZCC50'
                            },
                            {'Firstname': 'Donna',
                            'Lastname': 'Sheridan',
                            'date of birth': '04/04/1992',
                            'gender': 'female',
                            'voterID': 'SOW22TGOAL'
                            },
                            {'Firstname': 'Charlie',
                            'Lastname': 'Simms',
                            'date of birth': '05/05/1994',
                            'gender': 'male',
                            'voterID': 'D9219AL36'
                            },
                            {'Firstname': 'Bruce',
                            'Lastname': 'Wayne',
                            'date of birth': '09/08/1984',
                            'gender': 'male',
                            'voterID': 'DC1939T4UE'
                            },
                            {'Firstname': 'Laura',
                            'Lastname': 'Croft',
                            'date of birth': '05/04/1990',
                            'gender': 'female',
                            'voterID': 'VG90SPSXBO'
                            },
                            {'Firstname': 'Peter',
                            'Lastname': 'Parker',
                            'date of birth': '04/05/1998',
                            'gender': 'male',
                            'voterID': 'MC1962RT0S'
                            },
                            ]
        # Store voter voted
        self.voted_voter = []
        
        # Store information of each candidate
        self.candidates = [{'Candidate': 'A',
                            'Firstname': 'Biff',
                            'Lastname': 'Tannen',
                            'gender': 'male',
                            'date of birth': '01/02/1955',
                            'party': 'Republican'
                            },
                            {'Candidate': 'B',
                            'Firstname': 'Thomas',
                            'Lastname': 'Whitmore',
                            'gender': 'male',
                            'date of birth': '07/04/1970',
                            'party': 'Democratic'
                            }]
        
        # Store a list to count number of votes for each candidate
        self.count = {'A': 0, 'B': 0}
        
        # Store the number of voters
        self.voters = 0
        
    # function to create a block
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash':previous_hash,
                 'votes': self.votes
                }
        self.votes = []
        self.chain.append(block)
        return block
    
    # function to get the previous block
    def get_previous_block(self):
        return self.chain[-1]
    
    # function to calculate the proof of work
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    # function to hash the block
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    # function to check if the chain is valid
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
    # function to verify voter information to vote
    def verify_voter_info(self, firstname, lastname, DOB, gender, voterID):
        can_vote = False
         # input info to vote
        input = {'Firstname': firstname,
                 'Lastname': lastname,
                 'date of birth': DOB,
                 'gender': gender,
                 'voterID': voterID
                }
        for i in self.voter_data:
            if i == input:
                self.voter_data.remove(i)
                can_vote = True
        return can_vote
        
    # function to check and prevent the same voter from voting twice
    def verify_voted_voter(self, firstname, lastname, DOB, gender, voterID):
        cannot_vote = False
        input = {'Firstname': firstname,
         'Lastname': lastname,
         'date of birth': DOB,
         'gender': gender,
         'voterID': voterID
        }
        for i in self.voted_voter:
            if i == input:
                cannot_vote = True
        return cannot_vote

            
            
    # function to increment count for candidate
    def add_count(self, candidate):
        for i in self.count:
            if i == candidate:
                self.count[i] += 1
                self.voters += 1
    
    # function to add vote
    def add_vote(self, firstname, lastname, DOB, gender, voterID, candidate):
        # added to votes list
        self.votes.append({'Firstname': firstname,
                           'Lastname': lastname,
                           'date of birth': DOB,
                           'gender': gender,
                           'voterID': voterID,
                           'candidate': candidate
                           })
        # added to voted voter list
        self.voted_voter.append({'Firstname': firstname,
                                'Lastname': lastname,
                                'date of birth': DOB,
                                'gender': gender,
                                'voterID': voterID,
                                })
        self.add_count(candidate)
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    # function to register a voter
    def register_voter(self, firstname, lastname, DOB, gender, voterID):
        self.voter_data.append({'Firstname': firstname,
                                'Lastname': lastname,
                                'date of birth': DOB,
                                'gender': gender,
                                'voterID': voterID,
                                })
        
    
    # function to add node
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    # function to replace chain
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

# Part 2 - Mining our Blockchain   
    
# Create a Web App
app = Flask(__name__)

# Create an address for the node on Port 
node_address = str(uuid4()).replace('-', '')

# Create a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    #blockchain.add_vote(firstname = '', lastname = '', age = '', voterID = '', candidate = '')
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulation, you just mined a block!', 
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'votes': block['votes']
                }
    return jsonify(response), 200

# Getting result of election
@app.route('/get_result', methods = ['GET'])
def get_result():
    if blockchain.count['A'] > blockchain.count['B']:
        result = blockchain.count['A']
        response = {'message': f'Candadidate A: Biff Tannen has won the election with {result} votes.'}
    elif blockchain.count['B'] > blockchain.count['A']:
        result = blockchain.count['B']
        response = {'message': f'Candadidate B: Thomas Whitmore has won the election with {result} votes.'}
    else:
        response = {'message': 'Election results in a tie.'}
    return jsonify(response), 200

# Getting voters information
@app.route('/get_voter_details', methods = ['GET'])
def get_voter_details():
    response = blockchain.voter_data
    return jsonify(response), 200   
    
# Getting candidate information
@app.route('/get_candidates', methods = ['GET'])
def get_candidate():
    response = blockchain.candidates
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'voters': blockchain.voters,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

# Registering a voter to the blockchain
@app.route('/register_voter', methods = ['POST'])
def register_voter():
    json = request.get_json()
    vote_keys = ['Firstname', 'Lastname', 'date of birth', 'gender', 'voterID']
    if not all(key in json for key in vote_keys):
        return 'Some elements of the transaction are missing', 400
    else:
        blockchain.register_voter(json['Firstname'], json['Lastname'], json['date of birth'], json['gender'], json['voterID'])
        response = {'message':'voter added.'}
    return jsonify(response), 200
    

# Adding a new vote to the Blockchain
@app.route('/add_vote', methods = ['POST'])
def add_vote():
    json = request.get_json()
    vote_keys = ['Firstname', 'Lastname', 'date of birth', 'gender', 'voterID', 'candidate']
    if not all(key in json for key in vote_keys):
        return 'Some elements of the transaction are missing', 400
    if blockchain.verify_voter_info(json['Firstname'], json['Lastname'], json['date of birth'], json['gender'], json['voterID']):
        index = blockchain.add_vote(json['Firstname'], json['Lastname'], json['date of birth'], json['gender'], json['voterID'], json['candidate'])
        response = {'message':f'This vote will be added to Block {index}'}
    elif blockchain.verify_voted_voter(json['Firstname'], json['Lastname'], json['date of birth'], json['gender'], json['voterID']):
        response = {'message': 'You have already voted!'}
    else:
        response = {'message': 'Unable to verify data. Please try again!'}
    return jsonify(response), 201

# Part 3 - Decentralizing our Blockchain

# Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The e-voting Blockchain now contains the following nodes:',
                'nodes connected': list(blockchain.nodes)}
    return jsonify(response), 201

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200

# Running the app
app.run(host = '127.0.0.1', port = 5000)
