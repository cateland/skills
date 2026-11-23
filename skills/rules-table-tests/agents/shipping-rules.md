# The rules of the shipping fee

The shop calculates a shipping fee for each order. The fee comes from the cart and the destination.
`shipping.test.ts` runs every row of this file.

## Why these rules exist

The customer must know the fee before they pay. The fee must not surprise the customer.

A domestic delivery is free from the free subtotal. Thus a large order costs the customer less.

An express delivery costs more for the carrier. Thus an express delivery is never free.

A carrier does not fly a lithium battery out of the region. Thus the shop refuses such an order.
The shop does not take a payment for a delivery that it cannot do.

A pickup costs the shop nothing. Thus a pickup is always free. The shop never refuses a pickup.

## Terms

- **Cart**: the items of the order.
- **Subtotal**: the price of the cart before the shipping fee, in euros.
- **Destination**: the place where the order goes. It is a pickup, a domestic delivery or an
  abroad delivery.
- **Pickup**: the customer takes the order at the shop.
- **Domestic delivery**: a delivery in the country of the shop.
- **Abroad delivery**: a delivery to a zone out of the country.
- **Zone**: `eu` is a country of the European Union. `world` is a country out of the European Union.
- **Region**: the country of the shop and the `eu` zone.
- **Express**: a faster domestic delivery. It adds 10 euros to the fee.
- **Base fee**: the fee of a domestic delivery without express. It is 5 euros.
- **Free subtotal**: 50 euros. From this subtotal, a domestic delivery has no base fee.
- **Refused order**: an order that the shop cannot ship. A refused order has no fee.

## How to read this file

Each `##` heading gives one destination. The heading starts with the kind of destination. Then it
gives the options of the destination, for example `express yes` or `zone eu`.

Each row gives one cart and the two answers:

- `cart is`: how the cart is different from the usual cart. The usual cart has a subtotal of 20
  euros and no battery. An empty cell is the usual cart. The words are `subtotal N` and `battery`.
- `fee`: the fee in euros. `none` is the fee of a refused order.
- `refused`: `yes` when the shop refuses the order.

The text under a heading tells why the answers are correct. The test does not read this text.

# Fees

## pickup

| case                    | cart is | fee | refused |
|-------------------------|---------|-----|---------|
| a pickup is free        |         | 0   | no      |
| a pickup with a battery | battery | 0   | no      |

## domestic · express no

| case                                    | cart is     | fee | refused |
|-----------------------------------------|-------------|-----|---------|
| a cart below the free subtotal          | subtotal 49 | 5   | no      |
| a cart at the free subtotal             | subtotal 50 | 0   | no      |
| a cart with a battery inside the region | battery     | 5   | no      |

## domestic · express yes

An express delivery is never free. The free subtotal removes only the base fee.

| case                                    | cart is     | fee | refused |
|-----------------------------------------|-------------|-----|---------|
| an express cart below the free subtotal | subtotal 49 | 15  | no      |
| an express cart at the free subtotal    | subtotal 50 | 10  | no      |

## abroad · zone eu

| case                                    | cart is      | fee | refused |
|-----------------------------------------|--------------|-----|---------|
| a cart abroad is never free             | subtotal 500 | 15  | no      |
| a cart with a battery inside the region | battery      | 15  | no      |

## abroad · zone world

| case                                    | cart is | fee  | refused |
|-----------------------------------------|---------|------|---------|
| a cart out of the region                |         | 30   | no      |
| a cart with a battery out of the region | battery | none | yes     |
