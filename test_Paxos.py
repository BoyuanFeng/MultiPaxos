import sys
import unittest
import os.path

this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append( os.path.dirname(this_dir) )

from Paxos import *

PID = ProposalID

class ProposerTests(unittest.TestCase):

    at = unittest.TestCase.assertTrue
    ae = unittest.TestCase.assertEqual
    
    def am(self, msg, mtype, **kwargs):
        self.ae(msg.__class__.__name__.lower(), mtype)
        for k,v in kwargs.items():
            self.assertEqual(getattr(msg,k), v)

    # check if it is leader or not
    def al(self, value):
        if hasattr(self.p.leader, 'value'):
            self.assertEqual( self.p.leader, value)
            
    def promise_num(self):
        if hasattr(self.p, 'promises_received'):
            return len(self.p.promises_received)

    def setUp(self):
        self.p = Proposer('A', 2)

    def test_constructor(self):
        self.ae( self.p.network_uid, 'A' )
        self.ae( self.p.quorum_size, 2)

    def test_perpare(self):
        msg = self.p.prepare_Phase()
        self.am(msg, 'preparemsg', proposal_id = PID(1,'A'))
        self.al(False)

    def test_perpare_three(self):
        msg = self.p.prepare_Phase()
        self.am(msg, 'preparemsg', proposal_id = PID(1,'A'))
        msg = self.p.prepare_Phase()
        self.am(msg, 'preparemsg', proposal_id = PID(2,'A'))
        msg = self.p.prepare_Phase()
        self.am(msg, 'preparemsg', proposal_id = PID(3,'A'))
'''        
    def test_recv_promise_ignore_previous_proposal_value(self):
        self.p.prepare_Phase()
        self.p.prepare_Phase()
        self.p.prepare_Phase()
        self.p.receive( PromiseMsg('B', 'A', PID(3,'A'), PID(1,'B'), 'add') )
        self.p.prepare_Phase()
        self.p.receive( PromiseMsg('B', 'A', PID(4,'A'), PID(3,'B'), 'no') )
        self.ae( self.p.highest_accepted_id, PID(3,'B') )
        self.ae( self.p.proposed_value, 'no' )
        self.p.receive( PromiseMsg('C', 'C', PID(4,'A'), PID(2,'B'), 'no') )
        self.ae( self.p.highest_accepted_id, PID(3,'B') )
        self.ae( self.p.proposed_value, 'no' )
        
        
class AcceptorTests (unittest.TestCase):
    
    at = unittest.TestCase.assertTrue
    ae = unittest.TestCase.assertEqual
        
    def am(self, msg, mtype, **kwargs):
        self.ae(msg.__class__.__name__.lower(), mtype)
        for k,v in kwargs.items():
            self.assertEqual(getattr(msg,k), v)
    
    def setUp(self):        
        self.a = Acceptor('A')
     
    def test_recv_prepare_initial(self):
        self.ae( self.a.promised_id    , None)
        self.ae( self.a.accepted_value , None)
        self.ae( self.a.accepted_id    , None)
        m = self.a.receive( PrepareMsg('A', PID(1,'A')) )
        self.am(m, 'promise', proposer_uid='A', proposal_id=PID(1,'A'), last_accepted_id=None, last_accepted_value=None)
        
    def test_recv_accept_request_greater_than_promised(self):
        m = self.a.receive_prepare( PrepareMsg('A', PID(1,'A') ) )
        self.am(m, 'promise', proposer_uid='A', proposal_id=PID(1,'A'), last_accepted_id=None, last_accepted_value=None)

        m = self.a.receive( AcceptMsg('A', PID(5,'A'), 'foo') )
        self.am(m, 'accepted', proposal_id=PID(5,'A'), proposal_value='foo')


class PaxosInstanceTester (ProposerTests, AcceptorTests):

    def setUp(self):
        pla = PaxosInstance('A',2)
        self.p = pla
        self.a = pla
 '''       
if __name__ == '__main__':
    unittest.main()
