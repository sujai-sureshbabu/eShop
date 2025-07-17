
namespace OrderApi.Data;

using Microsoft.EntityFrameworkCore;
using OrderApi.Models;
public class OrderDbContext : DbContext
{
    public OrderDbContext(DbContextOptions<OrderDbContext> options) : base(options) { }

    public DbSet<Order> Orders { get; set; }
}
