g++ lzw.cpp -o lista3
start_time="$(date -u +%s.%N)"
./lista3 decode gamma encode.txt wynik2.txt
python3 lzw.py decode gamma wynik2.txt decode.txt
end_time="$(date -u +%s.%N)"

elapsed="$(bc <<<"$end_time-$start_time")"
diff test3.bin decode.txt
echo "Czas trwania: $elapsed"