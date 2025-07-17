namespace OrderService.Models;
public class Order
{
    public Guid Id { get; set; } = Guid.NewGuid();  // add default
    public string ProductId { get; set; } = string.Empty;
    public int Quantity { get; set; }
    public string Status { get; set; } = "PENDING";
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}
