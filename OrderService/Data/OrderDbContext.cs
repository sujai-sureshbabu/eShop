using Microsoft.EntityFrameworkCore;
using OrderService.Models; // Adjust the namespace to where your Order class is defined

public class OrderDbContext : DbContext
{
    public OrderDbContext(DbContextOptions<OrderDbContext> options) : base(options) { }

    public DbSet<Order> Orders { get; set; }
}
