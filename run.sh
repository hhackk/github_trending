cd /root/test/git
python git.py
python getnew.py
cd ../trending
cp ../git/lastnew.html index.html
git add index.html
git commit -m "log"
git push  origin master
cd -
