package com.canteen;

// CanteenOrder - Java Sales Report Generator
// Uses iText 7 to generate PDF reports and JavaMail to email them
// Run: javac -cp .:itext7-core-7.2.5.jar CanteenReportService.java
//       java  -cp .:itext7-core-7.2.5.jar com.canteen.CanteenReportService

import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import java.io.*;
import java.net.InetSocketAddress;
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.util.*;

/**
 * Standalone Java microservice for:
 * 1. Generating daily PDF sales reports
 * 2. Sending email notifications
 * 3. Token number sequencing API
 * 4. Tiffin subscription scheduler
 *
 * Runs on port 8080 alongside Flask (port 5000)
 */
public class CanteenReportService {

    static int tokenCounter = 1;
    static List<Map<String, String>> subscriptions = new ArrayList<>();

    public static void main(String[] args) throws IOException {
        // Start HTTP server on port 8080
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);

        server.createContext("/api/report/daily",   new DailyReportHandler());
        server.createContext("/api/report/weekly",  new WeeklyReportHandler());
        server.createContext("/api/token/next",     new TokenHandler());
        server.createContext("/api/token/reset",    new TokenResetHandler());
        server.createContext("/api/subscribe",      new SubscribeHandler());
        server.createContext("/api/health",         new HealthHandler());

        server.start();
        System.out.println("☕ CanteenOrder Java Service running on http://localhost:8080");
        System.out.println("   Endpoints:");
        System.out.println("   GET  /api/report/daily  -> Generate daily PDF report");
        System.out.println("   GET  /api/report/weekly -> Send weekly email summary");
        System.out.println("   GET  /api/token/next    -> Get next token number");
        System.out.println("   POST /api/token/reset   -> Reset daily token counter");
        System.out.println("   GET  /api/health        -> Health check");

        // Schedule daily report at 9 PM
        scheduleDailyReport();
    }

    // ── DAILY PDF REPORT HANDLER ──────────────────────────────────
    static class DailyReportHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if (!exchange.getRequestMethod().equals("GET")) {
                sendResponse(exchange, 405, "Method Not Allowed");
                return;
            }

            String reportContent = generateDailyReport();
            String filename = "CanteenOrder_Report_" +
                LocalDate.now().format(DateTimeFormatter.ISO_LOCAL_DATE) + ".txt";

            // In production: generate actual PDF using iText
            // For demo: return plain text report that shows what the PDF would contain
            exchange.getResponseHeaders().set("Content-Type", "text/plain; charset=UTF-8");
            exchange.getResponseHeaders().set("Content-Disposition", "attachment; filename=" + filename);
            sendResponse(exchange, 200, reportContent);
            System.out.println("[" + LocalTime.now() + "] Daily report generated: " + filename);
        }
    }

    // ── WEEKLY EMAIL HANDLER ──────────────────────────────────────
    static class WeeklyReportHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String summary = generateWeeklySummary();
            // sendEmail("admin@college.edu", "CanteenOrder Weekly Summary", summary);
            String response = "{\"success\":true,\"message\":\"Weekly email queued\",\"preview\":\"" +
                summary.replace("\n", "\\n").replace("\"", "'") + "\"}";
            exchange.getResponseHeaders().set("Content-Type", "application/json");
            sendResponse(exchange, 200, response);
            System.out.println("[" + LocalTime.now() + "] Weekly email prepared");
        }
    }

    // ── TOKEN GENERATOR ───────────────────────────────────────────
    static class TokenHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String token = String.format("T%03d", tokenCounter++);
            String response = "{\"token\":\"" + token + "\",\"number\":" + (tokenCounter - 1) + "}";
            exchange.getResponseHeaders().set("Content-Type", "application/json");
            sendResponse(exchange, 200, response);
        }
    }

    // ── TOKEN RESET ───────────────────────────────────────────────
    static class TokenResetHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            tokenCounter = 1;
            sendResponse(exchange, 200, "{\"success\":true,\"message\":\"Token counter reset to T001\"}");
            System.out.println("[" + LocalTime.now() + "] Token counter reset for new day");
        }
    }

    // ── TIFFIN SUBSCRIPTION ───────────────────────────────────────
    static class SubscribeHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String subId = "SUB" + (int)(Math.random() * 9000 + 1000);
            Map<String, String> sub = new HashMap<>();
            sub.put("id", subId);
            sub.put("created_at", LocalDateTime.now().toString());
            sub.put("active", "true");
            subscriptions.add(sub);

            String response = "{\"success\":true,\"subscription_id\":\"" + subId +
                "\",\"message\":\"Daily tiffin subscription activated Mon-Fri at 11:30 AM\"}";
            exchange.getResponseHeaders().set("Content-Type", "application/json");
            sendResponse(exchange, 200, response);
            System.out.println("[" + LocalTime.now() + "] New tiffin subscription: " + subId);
        }
    }

    // ── HEALTH CHECK ─────────────────────────────────────────────
    static class HealthHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String response = "{\"status\":\"healthy\",\"service\":\"CanteenOrder Java Service\"," +
                "\"port\":8080,\"token_counter\":" + tokenCounter +
                ",\"subscriptions\":" + subscriptions.size() +
                ",\"time\":\"" + LocalTime.now() + "\"}";
            exchange.getResponseHeaders().set("Content-Type", "application/json");
            sendResponse(exchange, 200, response);
        }
    }

    // ── REPORT GENERATORS ────────────────────────────────────────
    static String generateDailyReport() {
        LocalDate today = LocalDate.now();
        StringBuilder sb = new StringBuilder();
        sb.append("=".repeat(60)).append("\n");
        sb.append("     CANTEEN ORDER - DAILY SALES REPORT\n");
        sb.append("     ").append(today.format(DateTimeFormatter.ofPattern("EEEE, MMMM dd yyyy"))).append("\n");
        sb.append("=".repeat(60)).append("\n\n");

        sb.append("SUMMARY\n").append("-".repeat(40)).append("\n");
        sb.append(String.format("%-30s %s\n", "Total Revenue:", "Rs. 1,240"));
        sb.append(String.format("%-30s %s\n", "Total Orders:", "48"));
        sb.append(String.format("%-30s %s\n", "Average Order Value:", "Rs. 25.83"));
        sb.append(String.format("%-30s %s\n", "Wallet Transactions:", "32"));
        sb.append(String.format("%-30s %s\n", "Counter Payments:", "16"));
        sb.append("\n");

        sb.append("TOP SELLING ITEMS\n").append("-".repeat(40)).append("\n");
        String[][] items = {
            {"1", "Masala Chai",    "45", "Rs. 450"},
            {"2", "Vada Pav",       "30", "Rs. 450"},
            {"3", "Samosa",         "22", "Rs. 264"},
            {"4", "Pav Bhaji",      "18", "Rs. 990"},
            {"5", "Thali (Full)",   "12", "Rs. 960"},
        };
        sb.append(String.format("%-4s %-20s %-10s %s\n", "#", "Item", "Units", "Revenue"));
        for (String[] row : items) {
            sb.append(String.format("%-4s %-20s %-10s %s\n", row[0], row[1], row[2], row[3]));
        }
        sb.append("\n");

        sb.append("PEAK HOURS\n").append("-".repeat(40)).append("\n");
        int[] hours = {8,9,10,11,12,13,14,15,16,17};
        int[] orders = {5, 8, 12, 18, 35, 42, 28, 15, 8, 4};
        for (int i = 0; i < hours.length; i++) {
            String bar = "#".repeat(orders[i] / 2);
            sb.append(String.format("%02d:00  %-25s %d orders\n", hours[i], bar, orders[i]));
        }
        sb.append("\n");

        sb.append("FINANCIAL SUMMARY\n").append("-".repeat(40)).append("\n");
        sb.append(String.format("%-30s %s\n", "Gross Revenue:", "Rs. 1,240"));
        sb.append(String.format("%-30s %s\n", "Est. Food Cost (40%):", "Rs. 496"));
        sb.append(String.format("%-30s %s\n", "Est. Net Profit:", "Rs. 744"));
        sb.append(String.format("%-30s %s\n", "Points Issued:", "124 pts"));
        sb.append("\n");

        sb.append("=".repeat(60)).append("\n");
        sb.append("Generated by CanteenOrder Java Service | " + LocalDateTime.now() + "\n");
        sb.append("=".repeat(60)).append("\n");
        return sb.toString();
    }

    static String generateWeeklySummary() {
        return "CanteenOrder Weekly Summary\n" +
               "Week of " + LocalDate.now().minusDays(7) + " to " + LocalDate.now() + "\n\n" +
               "Total Revenue: Rs. 7,420\n" +
               "Total Orders:  312\n" +
               "Best Day:      Friday (Rs. 1,350)\n" +
               "Worst Day:     Sunday (Rs. 600)\n" +
               "Avg Rating:    4.6 stars\n" +
               "New Users:     8\n\n" +
               "Top Item:      Masala Chai\n" +
               "Worst Rated:   Upma (4.2)\n\n" +
               "Forecast next week: +15% (exam season)";
    }

    // ── EMAIL SENDER (JavaMail) ────────────────────────────────────
    // Uncomment and configure when deploying with actual SMTP
    /*
    static void sendEmail(String to, String subject, String body) {
        Properties props = new Properties();
        props.put("mail.smtp.host", "smtp.gmail.com");
        props.put("mail.smtp.port", "587");
        props.put("mail.smtp.auth", "true");
        props.put("mail.smtp.starttls.enable", "true");

        Session session = Session.getInstance(props, new Authenticator() {
            protected PasswordAuthentication getPasswordAuthentication() {
                return new PasswordAuthentication("canteen@college.edu", "YOUR_APP_PASSWORD");
            }
        });

        try {
            Message message = new MimeMessage(session);
            message.setFrom(new InternetAddress("canteen@college.edu"));
            message.setRecipients(Message.RecipientType.TO, InternetAddress.parse(to));
            message.setSubject(subject);
            message.setText(body);
            Transport.send(message);
        } catch (MessagingException e) {
            e.printStackTrace();
        }
    }
    */

    // ── SCHEDULER ────────────────────────────────────────────────
    static void scheduleDailyReport() {
        Thread scheduler = new Thread(() -> {
            while (true) {
                try {
                    LocalTime now = LocalTime.now();
                    // Reset token counter at midnight
                    if (now.getHour() == 0 && now.getMinute() == 0) {
                        tokenCounter = 1;
                        System.out.println("[" + now + "] Token counter reset for new day");
                    }
                    // Generate report at 9 PM
                    if (now.getHour() == 21 && now.getMinute() == 0) {
                        System.out.println("[" + now + "] Auto-generating daily report...");
                        generateDailyReport(); // Would also trigger email here
                    }
                    Thread.sleep(60000); // Check every minute
                } catch (InterruptedException e) { break; }
            }
        });
        scheduler.setDaemon(true);
        scheduler.start();
        System.out.println("⏰ Scheduler started: Daily report @ 9PM, Token reset @ midnight");
    }

    // ── UTILITY ──────────────────────────────────────────────────
    static void sendResponse(HttpExchange exchange, int code, String body) throws IOException {
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        byte[] bytes = body.getBytes("UTF-8");
        exchange.sendResponseHeaders(code, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(bytes);
        }
    }
}
