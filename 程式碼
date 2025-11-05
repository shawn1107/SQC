## ---------- R1 or R2：理論 + 模擬 + 圖表 ----------
set.seed(123)

Phi    <- pnorm
alpha1 <- 2 * (1 - Phi(3))                      # Rule1 單點型一錯誤
pA     <- Phi(-2) - Phi(-3)                     # Zone A（單側）
alpha2 <- 2 * (choose(3,2)*pA^2*(1-pA) + pA^3)  # Rule2 每個3點視窗型一錯誤

# 理論：長度 n 的序列內「至少一次」（R1 or R2）
theory_R1orR2 <- function(n){
  if (n < 3) return(1 - (1 - alpha1)^n)
  1 - ((1 - alpha1)^n) * ((1 - alpha2)^(n - 2))
}

# 規則（模擬用）
rule1 <- function(z) any(abs(z) > 3)
rule2 <- function(z){
  m <- length(z); if (m < 3) return(FALSE)
  A <- (abs(z) >= 2) & (abs(z) < 3)   # Zone A
  s <- sign(z)
  for (i in 1:(m-2)){
    w <- i:(i+2)
    if (sum(A[w] & (s[w] > 0)) >= 2) return(TRUE)  # 上側 ≥2
    if (sum(A[w] & (s[w] < 0)) >= 2) return(TRUE)  # 下側 ≥2
  }
  FALSE
}

# 模擬：同一段序列是否曾被 R1 或 R2 觸發
sim_R1orR2 <- function(n, reps = 10000){
  cnt <- 0L
  for (r in 1:reps){
    z <- rnorm(n)                         # in-control：Z ~ N(0,1)
    if (rule1(z) || rule2(z)) cnt <- cnt + 1L
  }
  cnt / reps
}

# 要評估的 n
ns <- c(1, 5, 10, 20, 50, 100)

# 結果表
res <- data.frame(
  n = ns,
  Theoretical_R1_or_R2 = sapply(ns, theory_R1orR2),
  Simulated_R1_or_R2   = sapply(ns, sim_R1orR2)
)

# 1) 印表（可直接貼到報告）
print(round(res, 6), row.names = FALSE)

# 2) 畫圖（理論 vs 模擬）
par(mar = c(4.5, 4.8, 3.5, 1) + 0.1)
ylim_range <- range(c(res$Theoretical_R1_or_R2, res$Simulated_R1_or_R2))

plot(res$n, res$Theoretical_R1_or_R2,
     type = "o", pch = 16, lwd = 2,
     xlab = "n (number of points)",
     ylab = "Probability of at least one false alarm",
     main = "R1 or R2 (Theoretical vs Simulation)",
     ylim = ylim_range)

lines(res$n, res$Simulated_R1_or_R2,
      type = "o", pch = 16, lwd = 2, col = "darkgreen")

legend("topleft",
       legend = c("Theoretical (R1 or R2)", "Simulated (R1 or R2)"),
       col = c("black", "darkgreen"), lwd = 2, pch = 16, bty = "n")

        
