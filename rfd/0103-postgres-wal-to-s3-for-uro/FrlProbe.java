import java.sql.*;
import java.util.*;

public class Probe {
    static long now() { return System.nanoTime(); }
    static void report(String name, List<Long> s) {
        Collections.sort(s);
        System.out.printf("FRL %-26s median=%8.3f ms  p99=%8.3f ms  n=%d%n",
            name, s.get(s.size()/2)/1e6, s.get((int)(s.size()*0.99))/1e6, s.size());
    }
    public static void main(String[] a) throws Exception {
        String base = "jdbc:relational://localhost:1111";
        // 1. catalog connection: create the schema template, database and schema
        try (Connection c = DriverManager.getConnection(base + "/__SYS?schema=CATALOG");
             Statement st = c.createStatement()) {
            try { st.execute("DROP DATABASE /FRL/bench"); } catch (Exception e) {}
            st.execute("CREATE SCHEMA TEMPLATE bench_tmpl "
                     + "CREATE TABLE identity(user_id bigint, handle string, PRIMARY KEY(user_id))");
            st.execute("CREATE DATABASE /FRL/bench");
            st.execute("CREATE SCHEMA /FRL/bench/main WITH TEMPLATE bench_tmpl");
            System.out.println("FRL schema created");
        }
        // 2. data connection
        try (Connection c = DriverManager.getConnection(base + "/FRL/BENCH?schema=MAIN")) {
            int N = 20000;
            long t0 = now();
            try (PreparedStatement ps = c.prepareStatement(
                    "INSERT INTO identity(user_id, handle) VALUES (?, ?)")) {
                for (int i = 0; i < N; i++) {
                    ps.setLong(1, i); ps.setString(2, "user" + i); ps.executeUpdate();
                }
            }
            System.out.printf("FRL insert %d rows          %8.1f ms total%n", N, (now()-t0)/1e6);

            List<Long> sel = new ArrayList<>();
            try (PreparedStatement ps = c.prepareStatement(
                    "SELECT handle FROM identity WHERE user_id = ?")) {
                for (int i = 0; i < 1000; i++) {
                    ps.setLong(1, i % N);
                    long s0 = now();
                    try (ResultSet rs = ps.executeQuery()) { rs.next(); }
                    sel.add(now()-s0);
                }
            }
            report("point SELECT", sel);

            List<Long> upd = new ArrayList<>();
            try (PreparedStatement ps = c.prepareStatement(
                    "UPDATE identity SET handle = ? WHERE user_id = ?")) {
                for (int i = 0; i < 1000; i++) {
                    ps.setString(1, "x"); ps.setLong(2, i % N);
                    long s0 = now(); ps.executeUpdate(); upd.add(now()-s0);
                }
            }
            report("point UPDATE", upd);
        }
    }
}
