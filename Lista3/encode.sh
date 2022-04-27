g++ lzw.cpp -o lista3
start_time="$(date -u +%s.%N)"
python3 lzw.py encode $1 $2 wynik.txt
./lista3 encode $1 wynik.txt encode.txt
end_time="$(date -u +%s.%N)"

elapsed="$(bc <<<"$end_time-$start_time")"
echo "Czas trwania kodowania: $elapsed"

first=$(stat -c%s "$2")
second=$(stat -c%s "encode.txt")

echo "$2 : ${first}"
echo "encode.txt : ${second}"

echo "Współczynnik kompresji: "
echo "scale=2 ; $first / $second" | bc