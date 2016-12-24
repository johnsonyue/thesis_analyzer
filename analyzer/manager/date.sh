data_dir=$(awk -F " *= *" '/data_dir/ {print $2}' config.ini) #configurable: directory of downloaded data
name=$(awk -F " *= *" '/name/ {print $2}' config.ini)
iplane_dir=$(awk -F " *= *" '/iplane_dir/ {print $2}' config.ini)
code_dir=$(awk -F " *= *" '/code_dir/ {print $2}' config.ini)
lg_dir=$(awk -F " *= *" '/lg_dir/ {print $2}' config.ini)
kapar_dir=$(awk -F " *= *" '/kapar_dir/ {print $2}' config.ini)

cat $data_dir"/manager_log" | grep "$name" | grep "finished" | awk '{print $4}'
