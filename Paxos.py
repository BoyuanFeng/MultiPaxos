import collections

#Create unique proposal ID by using Python tuples
ProposalID = collections.namedtuple('ProposalID', ['number', 'uid'])

class PaxosMsg(object):
    # Base class for all messages defined 
    from_uid = None

class PrepareMsg (PaxosMsg):
    def __init__(self, from_uid, proposal_id):
        self.from_uid   = from_uid
        self.proposal_id= proposal_id

class PromiseMsg (PaxosMsg):
    def __init__(self, from_uid, proposer_uid, proposal_id, last_accepted_id, last_accepted_value):
        self.from_uid            = from_uid
        self.proposer_uid        = proposer_uid
        self.proposal_id         = proposal_id
        self.last_accepted_id    = last_accepted_id
        self.last_accepted_value = last_accepted_value

class InvalidMessageError (Exception):
    '''
    Thrown if a PaxosMessage subclass is passed to a class that does not
    support it
    '''
    

class NackMsg (PaxosMsg):

    def __init__(self, from_uid, proposer_uid, proposal_id, promised_proposal_id):
        self.from_uid             = from_uid
        self.proposal_id          = proposal_id
        self.proposer_uid         = proposer_uid
        self.promised_proposal_id = promised_proposal_id


class AcceptMsg (PaxosMsg):
    def __init__(self, from_uid, proposal_id, proposal_value):
        self.from_uid       = from_uid
        self.proposal_id    = proposal_id
        self.proposal_value = proposal_value

class AcceptedMsg (PaxosMsg):
    def __init__(self, from_uid, proposal_id, proposal_value):
        self.from_uid       = from_uid
        self.proposal_id    = proposal_id
        self.proposal_value = proposal_value

class Final_value (PaxosMsg):
    
    # indicate that the final value has been selected
    def __init__(self, from_uid, value):
        self.from_uid = from_uid
        self.value    = value

class MessageHandler (object):

    def receive(self, msg):
        
       # Message dispatching function. This function accepts any PaxosMessage subclass and calls
       # the appropriate handler function
        
        handler = getattr(self, 'receive_' + msg.__class__.__name__.lower(), None)
        if handler is None:
            raise InvalidMessageError('Receiving class does not support messages of type: ' + msg.__class__.__name__)
        return handler( msg )
   

class Proposer (MessageHandler):

    leader               = False
    proposed_value       = None
    proposal_id          = None
    nacks_received       = None
    highest_accepted_id  = None
    promises_received    = None
    current_prepare_msg  = None
    current_accept_msg   = None
    

    def __init__(self, network_uid, quorum_size):
        self.network_uid         = network_uid
        self.quorum_size         = quorum_size
        self.proposal_id         = ProposalID(0, network_uid)
        self.highest_proposal_id = ProposalID(0, network_uid)
        self.final_value        = None
        self.final_acceptors    = None
        self.final_proposal_id  = None

    def propose_Value(self, value):
        #Sets the proposal value for this node if this node does not have any value
        if self.proposed_value is None:
            self.proposed_value = value

            if self.leader:
                self.current_accept_msg = AcceptMsg(self.network_uid, self.proposal_id, value)
                return self.current_accept_msg
            
    def prepare_Phase(self):
        # Returns a new Prepare message with a proposal id higher than that of
        # of any observed proposals.

        self.leader              = False
        self.promises_received   = set()
        self.nacks_received      = set()
        self.proposal_id         = ProposalID(self.highest_proposal_id.number + 1, self.network_uid)
        self.highest_proposal_id = self.proposal_id
        self.current_prepare_msg = PrepareMsg(self.network_uid, self.proposal_id)

        return self.current_prepare_msg

    def proposal_number(self, proposal_id):
        # Update the proposal counter as propsals are seen on the network.
        # Avoid a message dely when attempting to assume leadership and guaranteed
        # NACK if the proposal number is too low. Should automatically called for all
        # received Promise and Nack messages

        if proposal_id > self.highest_proposal_id:
            self.highest_proposal_id = proposal_id

    def receive_Nack(self, msg):
        # Return a new prepare message if the number of Nacks received reaches a quorum
        self.proposal_number( msg.promised_proposal_id )

        if msg.proposal_id == self.proposal_id and self_nacks_received is not None:
            self.nacks_received.add( msg.from_uid )

            if len(self.nacks_received) == self.quorum_size:
                # Lost leadership or failed to acquire it 
                return self.prepare_Phase()

        

    def receive_Promise(self, msg):
        # Return an accept msg if majority of promise msg is reached

        self.proposal_number( msg.proposal_id )

        if not self.leader and msg.proposal_id == self.proposal_id and msg.from_uid not in self.promises_received:
            
            # counts promises
            self.promises_received.add(msg.from_uid)

            # Updates highest accepted id
            if msg.last_accepted_id > self.highest_accepted_id:
                self.highest_accepted_id = msg.last_accepted_id
                # Updates value
                if msg.last_accepted_value is not None:
                    self.proposed_value = msg.last_accepted_value
            # Selects Leader
            if len(self.promises_received) == self.quorum_size:
                self.leader = True

                if self.proposed_value is not None:
                    self.current_accept_msg = AcceptMsg(self.network_uid, self.proposal_id, self.proposed_value)
                    return self.current_accept_msg
'''
    def receive_accepted_check (self, msg):
        # Called when an Accepted message is received from an acceptor. Determines
        # when the final value is selected and return the final value.

        if self.final_value is not None:
            if msg.proposal_id >= self.final_proposal_id and msg.proposal_value == self.final_value:
                self.final_acceptors.add( msg.from_uid )
            return Final_value (self.network_uid, self.final_value)
'''
class Acceptor(MessageHandler):

    def __init__(self, network_uid, promised_id=None, accepted_id=None, accepted_value=None):

        self.network_uid        = network_uid
        self.promised_id        = promised_id
        self.accepted_id        = accepted_id
        self.accepted_value     = accepted_value
 

    # Return a promise or nack in response
    def receive_prepare(self, msg):
        if msg.proposal_id >= self.promised_id:
            self.promised_id = msg.proposal_id
            return PromiseMsg(self.network_uid, msg.from_uid, self.promised_id, self.accepted_id, self.accepted_value)
        else:
            return NackMsg(self.network_uid, msg.from_uid, msg.proposal_id, self.promised_id)

    # Return accepted or nack msg in response      
    def receive_accept(self, msg):
        if msg.proposal_id >= self.promised_id:
            self.promised_id    = msg.proposal_id
            self.accepted_id    = msg.proposal_id
            self.accepted_value = msg.proposal_value
            return AcceptedMsg(self.network_uid, msg.proposal_id, msg.proposal_value)
        else:
            return NackMsg(self.network_uid, msg.from_uid, msg.proposal_id, self.promised_id)


        
class PaxosInstance (Proposer, Acceptor):

    def __init__(self, network_uid, quorum_size, promised_id=None, accepted_id=None, accepted_value=None):
        Proposer.__init__(self, network_uid, quorum_size)
        Acceptor.__init__(self, network_uid, promised_id, accepted_id, accepted_value)

    def receive_prepare(self, msg):
        self.proposal_number( msg.proposal_id )
        return super(PaxosInstance,self).receive_prepare(msg)
                    
    def receive_accept(self, msg):
        self.proposal_number( msg.proposal_id )
        return super(PaxosInstance,self).receive_accept(msg)        
        
        
