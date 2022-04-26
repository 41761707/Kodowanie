g++ lzw.cpp -o lista3
start_time="$(date -u +%s.%N)"
python3 lzw.py encode gamma test3.bin wynik.txt
./lista3 encode gamma wynik.txt encode.txt
end_time="$(date -u +%s.%N)"

elapsed="$(bc <<<"$end_time-$start_time")"
echo "Czas trwania: $elapsed"