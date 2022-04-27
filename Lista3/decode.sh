g++ lzw.cpp -o lista3
start_time="$(date -u +%s.%N)"
./lista3 decode $1 encode.txt wynik2.txt
python3 lzw.py decode $1 wynik2.txt decode.txt
end_time="$(date -u +%s.%N)"

elapsed="$(bc <<<"$end_time-$start_time")"
diff $2 decode.txt
echo "Czas trwania dekodowania: $elapsed"