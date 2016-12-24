import request_handler
import config
import time
import signal
import sys
import threading
import os

date = "";
data_source = "";
mt_num = 10
handler = request_handler.RequestHandler("config.ini");

def usage():
	print "python run.py caida/iplane/lg"
	exit()

def analyze_thread(date, source, out_dir):
	start_time = time.time();
	print handler.notify_started(date,data_source);
	sys.stdout.flush()

	os.makedirs(out_dir + "/" + date)
	os.system('bash -c "echo %s | ./dump.sh %s | python file2trace.py %s | python dump_graph.py" >%s/%s/%s.graph' % (date, source, source ,out_dir, date, date) )
	print ('"bash -c "echo %s | ./dump.sh %s | python file2trace.py %s | python dump_graph.py" >%s/%s/%s.graph' % (date, source, source ,out_dir, date, date) )

	end_time = time.time();
	time_used = end_time - start_time;
	print handler.notify_finished(date, time_used, data_source);
	sys.stdout.flush()

def get_alive_thread_cnt(th_pool):
	cnt_alive = 0;
        for i in range(len(th_pool)):
                t = th_pool[i];
                if (t.is_alive() ):
                        cnt_alive = cnt_alive + 1;
        for th in th_pool:
                if (not th.is_alive()):
                        th_pool.remove(th);

        return cnt_alive;

def main(argv):
	if len(argv) < 2:
		usage()
	
	global date
	global data_source
	data_source = argv[1]
	
	valid_source = ["caida", "iplane"]
	if not data_source in valid_source:
		usage()

	out_dir = config.get_config_section_dict("config.ini", "data")["out_dir"]
	th_pool = []
	while(True):
		date = handler.get_task(data_source);
		print date;
		sys.stdout.flush()
		
		th = threading.Thread( target=analyze_thread, args=(date, data_source, out_dir, ) )
		th_pool.append(th)
		th.start()
		time.sleep(4)
		
		time.sleep(1)
		
		while (get_alive_thread_cnt(th_pool) >= mt_num):
			time.sleep(1)
			
if __name__ == '__main__':
	main(sys.argv)
