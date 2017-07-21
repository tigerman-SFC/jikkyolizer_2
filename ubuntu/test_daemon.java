package com.tasknotes.daemon;

import org.apache.commons.daemon.Daemon;
import org.apache.commons.daemon.DaemonContext;
import org.apache.commons.daemon.DaemonInitException;

public class TestDaemon implements Daemon {

  private Thread thread; 
  private boolean stopped = false;

  @Override
  public void start() throws Exception {
    thread.start();
  }

  @Override
  public void stop() throws Exception {
    stopped = true;
    try {
      thread.join();
    } catch (InterruptedException e) {
      System.err.println(e.getMessage());
      throw e;
    }
  }

  @Override
  public void destroy() {
    thread = null;
  }

  @Override
  public void init(DaemonContext daemonContext) throws DaemonInitException, InterruptedException, Exception {
    thread = new Thread() {
      private long i = 0;
      @Override
      public void run() {
        while(!stopped) {
          System.out.println(i++);
          try {
            sleep(1000);
          } catch (InterruptedException e) {
            System.err.println(e.getMessage());
          }
        }
      }
    };
  }
}