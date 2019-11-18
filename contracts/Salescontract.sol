pragma solidity >= 0.5.11;

contract SalesContract {
    address public owner;
    uint256 public updatedTime;
    string public  salesDescription;
    uint public price;
    bool public onSale = true;
    
    event UserStatus(string _msg, address user, uint amount, uint256 time);
    
    constructor (string memory description, uint _price) public payable {
        owner = msg.sender;
        salesDescription = description;
        price = _price;
        updatedTime = block.timestamp;
        emit UserStatus(description, msg.sender, msg.value, block.timestamp);
        emit UserStatus("Item on Sale: ", msg.sender, msg.value, block.timestamp);
    }
    function getDescription() public view returns (string memory) {
        return salesDescription;
    }
    
    function getPrice() public view returns (uint){
        return price;
    }
    
    function getOwner() public view returns (address){
        return owner;
    }
    
    function getOnSale() public view returns (bool){
        return onSale;
    }
    
    function setDescription(string memory _description) public {
        salesDescription = _description;
    }
    
    function setPrice(uint _price) public{
        price = _price;
    }
    
    function setOwner(address user) public{
        owner = user;
    }
    
    function buy()  public payable {
        if(msg.value >= price && onSale == true){
            address(this).balance;
            owner = msg.sender;
            onSale = false;
            emit UserStatus("Item Bought", msg.sender, msg.value, block.timestamp);
            emit UserStatus("Item No Longer on Sale", msg.sender, msg.value, block.timestamp);
            
        }
        else{
            revert();
        }
        updatedTime = block.timestamp;
    }
    
    function updatePrice(uint _price) public onlyOwner{
        price = _price;
        emit UserStatus("Price Updated", msg.sender, price, block.timestamp);
    }
    
    function modifyDescription(string memory description) public onlyOwner {
        salesDescription = description;
        emit UserStatus(description, msg.sender, 0, block.timestamp);
    }
    
    function putOnSale() public onlyOwner {
        onSale = true;
        emit UserStatus("Item Now is on sale",   msg.sender, 0, block.timestamp);
    }
    
    function removeFromSale() public onlyOwner{
        onSale = false;
        emit UserStatus("Item no Longer on Sale", msg.sender, 0, block.timestamp);
    }
    
    modifier onlyOwner{
        updatedTime= block.timestamp;
        if (msg.sender != owner){
            revert();
        }
        else{
            _;
        }
    }
}