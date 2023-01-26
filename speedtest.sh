a=$(speedtest --list| grep -oh "\w*\w*[0-9])" | tr ")" " " | tr -d '\n')
test=${a%\,}
num=0
echo "No, Server ID, Hosted, Upload, Download" > speedtest_05.csv
echo "aTest Branch Feature"
for str in ${test[@]}; do
	((num++))
	echo "No. "$num" Server ID "$str
	info=$(speedtest --server $str)
	host=&(grep -i "Hosted" <<< $info | tr -d '.')
	echo $host
	up=&(grep -i "Upload" <<< $info | tr -d '.')
	echo $up
	down=&(grep -i "Download" <<< $info | tr -d '.')
	echo $down
	echo $num,$str,$host,$up,$down >> speedtest_05.csv
done
