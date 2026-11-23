export type Cart = { readonly subtotal: number; readonly battery: boolean };
export type Destination =
  | { readonly kind: 'pickup' }
  | { readonly kind: 'domestic'; readonly express: boolean }
  | { readonly kind: 'abroad'; readonly zone: 'eu' | 'world' };
export type Fee = { readonly kind: 'fee'; readonly euros: number } | { readonly kind: 'refused' };

export function shippingFee({ cart, destination }: { readonly cart: Cart; readonly destination: Destination }): Fee {
  switch (destination.kind) {
    case 'pickup':
      return { kind: 'fee', euros: 0 };
    case 'domestic':
      return { kind: 'fee', euros: (cart.subtotal >= 50 ? 0 : 5) + (destination.express ? 10 : 0) };
    case 'abroad':
      if (destination.zone === 'world' && cart.battery) return { kind: 'refused' };
      return { kind: 'fee', euros: destination.zone === 'eu' ? 15 : 30 };
    default: {
      const _exhaustive: never = destination;
      return _exhaustive;
    }
  }
}
