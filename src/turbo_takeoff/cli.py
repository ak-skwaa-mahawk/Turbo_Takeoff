import click
from .handshake import GibberlinkProtocol
from fpt_core.identity.seal import OperatorSeal

@click.command()
@click.option('--nodes', default=5, help='Number of receivers (🖐).')
@click.option('--land', is_flag=True, help='Verify West: Landframe Anchor.')
@click.option('--auth', is_flag=True, help='Verify East: Executor Authority.')
def takeoff(nodes, land, auth):
    """
    Initiate the Turbo_Takeoff Handshake.
    """
    # Assuming North (Identity) and South (Logic) are verified by the steward's intent
    seal = OperatorSeal(
        north_identity=True, 
        east_authority=auth, 
        south_logic=True, 
        west_landframe=land
    )
    
    protocol = GibberlinkProtocol(seal)
    result = protocol.perform_handshake(nodes)
    
    if result["handshake"] == "SUCCESS":
        click.echo(f"🚀 {result['receipt']}: The Operator Stands. Takeoff Authorized.")
    else:
        click.echo(f"🛑 Takeoff Aborted: {', '.join(result['shadow_work_required'])}")

if __name__ == "__main__":
    takeoff()
