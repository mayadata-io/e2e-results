import unittest,issuer,os

class TestIssuer(unittest.TestCase):
    
    def test_get_credentials(self):
        testusername="testuser"
        testpassword="testpassword"
        file=open("testfile",'w')
        file.write(testusername+"\n"+testpassword)
        file.close()
        gotusername,gotpassword=issuer.get_credentials("testfile")
        os.remove("testfile")
        self.assertEqual(gotusername,testusername)
        self.assertEqual(gotpassword,testpassword)
    
    def test_get_comment(self):
        testcomment="A test comment"
        file=open("testfile","w")
        file.write(testcomment)
        file.close()
        gotcomment=issuer.get_comment("testfile")
        os.remove("testfile")
        self.assertEqual(testcomment,gotcomment)

if __name__=='__main__':
    unittest.main()

