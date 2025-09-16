line_number=$(grep -wn EXAMPLE $2 | cut -d : -f 1)
line_number=$(($line_number+2))
head -n $line_number $2
sed -i "${line_number},\$d" $2

cat $1 >> $2
echo "Files copied!"
sed -i 's/H/Si/g' $2
echo "Symbols changed!"
