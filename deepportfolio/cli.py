import click
import mlconfig
import torch


@click.group()
def cli():
    pass


@cli.command(name='train')
@click.option('-c', '--config-file', default='configs/default.yaml')
def train(config_file):
    cfg = mlconfig.load(config_file)

    device = torch.device(cfg.device)

    model = cfg.model()
    model.to(device)

    loss_fn = cfg.loss_fn()

    optimizer = cfg.optimizer(model.parameters())
    scheduler = cfg.scheduler(optimizer)

    train_loader = cfg.train_loader()
    valid_loader = cfg.valid_loader()

    trainer = cfg.trainer(
        device=device,
        model=model,
        loss_fn=loss_fn,
        optimizer=optimizer,
        scheduler=scheduler,
        train_loader=train_loader,
        valid_loader=valid_loader,
    )
    trainer.fit()


if __name__ == '__main__':
    cli()
