YEAR_FROM=2017
YEAR_TO=2020
itr=0
for year in `seq $YEAR_FROM $YEAR_TO`; do
    echo $year
    curl -s localhost:8000/calendar/${year} > missal1962/static/data/${year}
    while [ 1 ]; do
        my_date=`date -j -v +${itr}d -f "%Y-%m-%d" $YEAR_FROM"-01-01" +%Y-%m-%d`
        if [[ $my_date == ${YEAR_TO}* ]]; then
            exit
        fi
        echo ${my_date}
        curl -s localhost:8000/date/${my_date} > missal1962/static/data/${my_date}
        itr=$(( itr + 1 ))
    done
done
