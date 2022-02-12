// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";

contract NftMinter is ERC721Enumerable {
    using Strings for uint256;
    address payable public owner;
    bool killSwitch;
    uint256 public price;
    uint256 soldId;

    mapping(uint256 => string) private _tokenURIs;
    uint256 public nftsMinted;

    uint256 public totalCurrentlyMintable;
    uint256 totalLimit = 10000;

    bool revealed;

    // Base URI
    string private _baseURIextended = "https://gateway.pinata.cloud/ipfs/";
    string private CID = "QmXKqmzGt6WmEBoTQN38FPiLPvugGPhqQjTXbEfQ8JVF4x/";

    constructor(string memory _CollectionName, string memory _symbol)
        ERC721(_CollectionName, _symbol)
    {
        killSwitch = false;
        nftsMinted = 0;
        owner = payable(msg.sender);

        totalCurrentlyMintable = 0;
    }

    function setMintFee(uint256 _newPrice) public onlyOwner {
        price = _newPrice;
    }

    function getPrice() public view returns (uint256) {
        return price;
    }

    function getTotalMinted() public view returns (uint256) {
        return nftsMinted;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }

    function Reveal() public onlyOwner {
        revealed = true;
    }

    function flipSaleState() public onlyOwner {
        killSwitch = !killSwitch;
    }

    function setBaseURI(string memory baseURI_) external onlyOwner {
        _baseURIextended = baseURI_;
    }

    function _setTokenURI(uint256 tokenId, string memory uri) internal virtual {
        require(
            _exists(tokenId),
            "ERC721Metadata: URI set of nonexistent token"
        );
        _tokenURIs[tokenId] = uri;
    }

    function _baseURI() internal view virtual override returns (string memory) {
        return _baseURIextended;
    }

    function tokenURI(uint256 tokenId)
        public
        view
        virtual
        override
        returns (string memory)
    {
        require(
            _exists(tokenId),
            "ERC721Metadata: URI query for nonexistent token"
        );

        string memory _tokenURI = _tokenURIs[tokenId];
        string memory base = _baseURI();

        if (!revealed) {
            return
                string(abi.encodePacked(base, "SomeHashForDefaultImage.JSON"));
        } else {
            return string(abi.encodePacked(base, CID, _tokenURI, ".JSON"));
        }
    }

    function mint(uint256 _amount) public payable {
        require(
            killSwitch == false,
            "This function is not available at this time"
        );

        if (msg.sender != owner) {
            require(msg.value >= price * _amount, "Not enough ether was sent");
            owner.transfer(msg.value);
        }
        require(_amount <= 10, "You can not mint more than 10 at a time");

        require(
            nftsMinted + _amount <= totalCurrentlyMintable,
            "Can not mint more than the limit"
        );

        for (uint256 i = 0; i < _amount; i++) {
            nftsMinted = nftsMinted + 1;
            _mint(msg.sender, nftsMinted);
            _setTokenURI(nftsMinted, nftsMinted.toString());
        }
    }

    function setOwner(address _to) public onlyOwner {
        owner = payable(_to);
    }

    function walletOfOwner(address queryWallet)
        public
        view
        returns (uint256[] memory)
    {
        uint256 ownerTokenCount = balanceOf(queryWallet);
        uint256[] memory tokenIds = new uint256[](ownerTokenCount);
        for (uint256 i; i < ownerTokenCount; i++) {
            tokenIds[i] = tokenOfOwnerByIndex(queryWallet, i);
        }
        return tokenIds;
    }

    function enableBatch(uint256 _amount, uint256 _price) public onlyOwner {
        price = _price;
        totalCurrentlyMintable = nftsMinted + _amount;
        require(
            totalCurrentlyMintable <= totalLimit,
            "You can not enable mint for more than the total allowed"
        );
    }

    function changeCID(string memory _newCID) public onlyOwner {
        CID = _newCID;
    }
}
